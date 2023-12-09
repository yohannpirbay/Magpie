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
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, TeamForm
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



def accept_or_decline_invite(request, invite_id, action):
    invite = Invite.objects.get(id=invite_id)
    if invite.recipient == request.user:
        if action == 'accept':
            invite.status = 'accepted'
            invite.save()
            invite.team.members.add(request.user)
            invite.team.save()
            request.user.add_team(invite.team)
            request.user.save()
        elif action == 'decline':
            invite.status = 'declined'
            invite.save()

    return JsonResponse({'message': 'Invitation updated successfully'})


@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    # User username is required for sorting tasks by assignedUsername
    current_userName = request.user.username

    # By default tasks and teams are in ascending order
    sort_order = request.GET.get('sort_order', 'ascending')
    sort_by_team = request.GET.get('sort_order_team', 'ascending')

    # Get the user's invitations
    invitations = Invite.objects.filter(recipient=current_user)
    sent_invitations = Invite.objects.filter(
        sender=current_user, status='pending')  # Query sent invitations by the user

    received_invitations = Invite.objects.filter(
        recipient=current_user, status='pending')

    context = {
        'sent_invitations': sent_invitations,
        'received_invitations': received_invitations,
        'user': current_user,
        
        # Other context variables
    }

    return render(request, 'dashboard.html', context)


'''Managing the accept invite and decline invite  and adding it into dashboard.html'''


@login_required
def accept_invite(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    if invite.recipient == request.user:
        # Update the status to "accepted"
        invite.status = 'accepted'
        invite.save()
        invite.team.members.add(request.user)
        print("I AM INSIDE ACCEPT INVITE VIEW")
        # Add the team to the user's teams
        request.user.teams.add(invite.team)

    # Redirect back to the dashboard
    return redirect('dashboard')


@login_required
def decline_invite(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    if invite.recipient == request.user:
        # Update the status to "declined"
        invite.status = 'declined'
        invite.save()
    return redirect('dashboard')


@login_required
def send_invitation(request, user_id):
    if request.method == 'POST':
        form = InvitationForm(request.POST, user=request.user)

        if form.is_valid():
            # Get the selected user, team, and the logged-in sender
            user = form.cleaned_data['user']
            team = form.cleaned_data['team']
            sender = request.user
            status = 'pending'  # You can set the default status here

            try:
                # Create a new Invite instance
                invite = Invite(sender=sender, recipient=user,
                                team=team, status=status)

                # Save the invitation to the database
                invite.save()

                # Add the invite to the sender's and recipient's sent and received invites
                sender.sent_invites.add(invite)
                user.received_invites.add(invite)

                # Optionally, send notifications or emails to the recipient

                # Redirect to a success page or back to the dashboard
                messages.success(request, 'Invitation sent successfully!')
                return redirect('dashboard')

            except Exception as e:
                # Log the exception for debugging
                messages.error(request, f"An error occurred: {e}")

        else:
            # Add an error message if the form is not valid
            error_message = ''
            for field, errors in form.errors.items():
                for error in errors:
                    error_message += mark_safe(f'{field.capitalize()}: {error}')

            messages.error(request, error_message)
    else:
        form = InvitationForm(user=request.user)

    context = {
        'form': form,
        'user_teams': request.user.teams.all(),
        'users': User.objects.all()
    }

    return render(request, 'send_invitation.html', context)


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


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
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


# @login_required()
# def create_team_view(request):
#     """Display the team creation screen and handles team creations."""
#
#     if request.method == 'POST':
#         form = TeamForm(request.POST)
#         if form.is_valid():
#             team = form.save()
#             return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
#     else:
#         form = TeamForm()
#     return render(request, 'create_team.html', {'form': form})


@login_required
def team_members(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    # Ensure the user is a member of the team
    if request.user.teams.filter(id=team_id).exists():
        members = team.members.all()
        return render(request, 'team_members.html', {'team': team, 'members': members})
    else:
        messages.error(
            request, "You are not authorized to view this team's members.")
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
                        team.members.add(selected_user)

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

    current_user = request.user

    # Get the user's invitations
    invitations = Invite.objects.filter(recipient=current_user)
    sent_invitations = Invite.objects.filter(
        sender=current_user, status='pending')  # Query sent invitations by the user

    received_invitations = Invite.objects.filter(
        recipient=current_user, status='pending')

    context = {
        'sent_invitations': sent_invitations,
        'received_invitations': received_invitations,
        'user': current_user,
        # Other context variables
    }

    return render(request, 'invites.html', context)


def My_team(request):

    return render(request, 'My_team.html')
