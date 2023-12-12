from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, TeamForm, TaskForm
from tasks.helpers import login_prohibited
from .models import Team, Invite, User,  Achievement  # Import your Team model
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import InvitationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils.safestring import mark_safe
from .signals import team_created_achievement  # Import your signal
from .models import Task
from django.http import Http404
from django.utils import timezone


@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    
    # Retrieve the current logged-in user
    current_user = request.user
    
    # User username is required for sorting tasks by assignedUsername
    current_userName = request.user.username

    # Get the user's invitations
    invitations = Invite.objects.filter(recipient=current_user)
    sent_invitations = Invite.objects.filter(
        sender=current_user, status='pending')  # Query sent invitations by the user

    received_invitations = Invite.objects.filter(
        recipient=current_user, status='pending')

    pending_invites_count = Invite.objects.filter(recipient=current_user, status='pending').count()

 
    # Retrieve tasks only assigned to the current user and from the specific teams
    tasks = Task.objects.filter(
        assigned_users=current_user, team__members=current_user)

    # Retrieve tasks assigned to the current user
    user_tasks = Task.objects.filter(assigned_users=current_user)


    # Retrieve the user's achievements
    user_achievements = current_user.achievements.all()
    
    # Prepare the context dictionary to pass data to the template
    context = {
        'sent_invitations': sent_invitations,
        'received_invitations': received_invitations,
        'user': current_user,
        'user_tasks': user_tasks,
        'achievements': user_achievements,
        'pending_invites_count': pending_invites_count,

        # Other context variables
    }

    # Render the dashboard template with the context data
    return render(request, 'dashboard.html', context)


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


# Decorator indicating that only logged-in users can access this view
@login_required
def send_invitation(request, user_id):
    # Check if the request method is POST
    if request.method == 'POST':
        # Create an InvitationForm instance with the submitted data and the logged-in user
        form = InvitationForm(request.POST, user=request.user)
        
        # Check if the form is valid
        if form.is_valid():
            try:
                # Create and save the invitation using a helper function
                invite = create_and_save_invitation(request.user, form.cleaned_data['user'], form.cleaned_data['team'])
                
                # Send an invitation notification (if needed)
                send_invitation_notification(invite.recipient)
                
                # Display a success message and redirect to the dashboard
                messages.success(request, 'Invitation sent successfully!')
                return redirect('dashboard')
            except Exception as e:
                # Display an error message if an exception occurs during the invitation process
                messages.error(request, f"An error occurred: {e}")
        else:
            # Handle form errors and display error messages
            handle_form_errors(request, form)
    else:
        # Create a new empty InvitationForm instance for rendering the form
        form = InvitationForm(user=request.user)

    # Prepare the context dictionary to pass data to the template
    context = {
        'form': form,
        'user_teams': request.user.teams.all(),
        'users': User.objects.all()
    }

    # Render the send_invitation.html template with the context data
    return render(request, 'send_invitation.html', context)




# Decorator indicating that only logged-in users can access this view
@login_required
def accept_invite(request, invite_id):
    # Retrieve the invitation object based on the provided ID
    invite = Invite.objects.get(id=invite_id)
    
    # Check if the logged-in user is the recipient of the invitation
    if invite.recipient == request.user:
        # Update the invitation status to 'accepted'
        invite.status = 'accepted'
        invite.save()
        
        # Add the user to the team associated with the invitation
        invite.team.members.add(request.user)
        
        # Add the team to the user's teams
        request.user.teams.add(invite.team)

    # Redirect back to the dashboard
    return redirect('dashboard')


# Decorator indicating that only logged-in users can access this view
@login_required
def decline_invite(request, invite_id):
    # Retrieve the invitation object based on the provided ID
    invite = Invite.objects.get(id=invite_id)
    
    # Check if the logged-in user is the recipient of the invitation
    if invite.recipient == request.user:
        # Update the invitation status to 'declined'
        invite.status = 'declined'
        invite.save()

    # Redirect back to the dashboard
    return redirect('dashboard')




# New helper functions

def create_and_save_invitation(sender, recipient, team):
    # Check if the user is already a member of the team
    if recipient in team.members.all():
        # If already a team member
        pass
    else:
        status = 'pending'
        invite = Invite(sender=sender, recipient=recipient, team=team, status=status)
        invite.save()
        sender.sent_invites.add(invite)
        recipient.received_invites.add(invite)
        return invite

def send_invitation_notification(user):
    # Implementation of sending notification (if needed)
    pass

def handle_form_errors(request, form):
    error_message = ''
    for field, errors in form.errors.items():
        for error in errors:
            error_message += mark_safe(f'{field.capitalize()}: {error}')
    messages.error(request, error_message)



class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get(
            'next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(
            self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(
            self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        """Handle form submission when valid."""
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after successful sign-up."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


@login_required
def team_members(request, team_id):
    # Retrieve the team object or return a 404 response if not found
    team = get_object_or_404(Team, pk=team_id)

    # Ensure the current user is a member of the specified team
    if request.user.teams.filter(id=team_id).exists():
        # If authorized, get the members of the team
        members = team.members.all()
        
        # Render the 'team_members.html' template with the team and its members
        return render(request, 'team_members.html', {'team': team, 'members': members})
    else:
        # If not authorized, display an error message and redirect to the dashboard
        messages.error(request, "You are not authorized to view this team's members.")
        return redirect('dashboard')



@login_required
def create_team_view(request):
    """Display the team creation screen and handle team creations."""
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Pass the user information to the form
                    team = form.save(commit=False, user=request.user)
                    team.save()  # Save the team first to get an ID

                    # Add the selected users to the team's members
                    for selected_user in form.cleaned_data['members']:
                        if selected_user != request.user:
                            create_and_save_invitation(request.user, selected_user, team)

                        # Add the creator to the team directly
                    team.members.add(request.user)
                    team.save()
                    
                    request.user.add_team(team)
                    request.user.save()

                    # Call the team_created_achievement signal manually
                    team_created_achievement(sender=request.user.__class__, instance=request.user, created=True)

                    # Check if it's the user's first team and award the achievement
                    if request.user.teams_joined.count() == 1:
                        achievement, created = Achievement.objects.get_or_create(name="First Team Created")
                        if created:
                            request.user.achievements.add(achievement)

                    # Add a success message
                    messages.success(request, 'Team created successfully!')
                    return redirect('dashboard')
            except Exception as e:
                # Log the exception e here for debugging
                messages.error(request, f"An error occurred: {e}")
        else:
            # Add an error message if the form is not valid
            messages.error(request, 'There was an error creating the team.')
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})



@login_required
def invites_view(request):
    """Display team invitations sent to user"""

    # Get the currently logged-in user
    current_user = request.user

    # Get the user's received invitations
    invitations = Invite.objects.filter(recipient=current_user)

    # Query sent invitations by the user with 'pending' status
    sent_invitations = Invite.objects.filter(sender=current_user, status='pending')

    # Query received invitations by the user with 'pending' status
    received_invitations = Invite.objects.filter(recipient=current_user, status='pending')

    # Prepare the context dictionary to pass data to the template
    context = {
        'sent_invitations': sent_invitations,
        'received_invitations': received_invitations,
        'user': current_user,
        # Other context variables can be added here
    }

    # Render the 'invites.html' template with the provided context
    return render(request, 'invites.html', context)


def My_team(request):

    return render(request, 'My_team.html')







def get_users_for_team(request, team_id):
    try:
        # Fetch the team based on the provided ID
        team = get_object_or_404(Team, id=team_id)

        # Get the users associated with the team
        users = team.members.all()

        # Create a JSON response with user data
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        

        return JsonResponse(user_data, safe=False)
    except Team.DoesNotExist:
        raise Http404("Team does not exist")
    
    
    
@login_required
def create_task(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a TaskForm instance with the POST data
        form = TaskForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            try:
                # Use a transaction to ensure atomicity
                with transaction.atomic():
                    # Create a task object without saving it to the database
                    task = form.save(commit=False)
                    task.save()
                    # Set the assigned_user field
                    task.assigned_users.set(form.cleaned_data['assigned_users'])
                    

                    # Display success message and redirect to the dashboard
                    messages.success(request, 'Task created successfully!')
                    return redirect('dashboard')
            except (User.DoesNotExist, ValueError, Exception) as e:
                # Handle exceptions and display an error message
                messages.error(request, f"An error occurred: {e}")
        else:
            # Display an error message if the form is not valid
            messages.error(request, 'There was an error creating the task.')
    else:
        # If the request method is not POST, create an empty TaskForm
        form = TaskForm()

        # Set the initial value for the team field based on the form's instance
        if form.instance and hasattr(form.instance, 'team') and form.instance.team:
            form.fields['team'].initial = str(form.instance.team.id)
        else:
            form.fields['team'].initial = ''

    # Render the create_task.html template with the form
    return render(request, 'create_task.html', {'form': form})


def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Your logic to update the task status
    task.is_finished = True
    task.finished_on = timezone.now()  # Record the finished_on time
    task.save()

    return JsonResponse({'success': True})

