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
from .models import Team, Invite, User # Import your Team model
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import InvitationForm
from django.http import JsonResponse

def accept_or_decline_invite(request, invite_id, action):
    invite = Invite.objects.get(id=invite_id)
    if invite.recipient == request.user:
        if action == 'accept':
            invite.status = 'accepted'
            invite.save()
            request.user.teams.add(invite.team)
        elif action == 'decline':
            invite.status = 'declined'
            invite.save()

    return JsonResponse({'message': 'Invitation updated successfully'})



@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user

    # Get the user's invitations
    invitations = Invite.objects.filter(recipient=current_user)
    sent_invitations = Invite.objects.filter(sender=current_user, status='pending')  # Query sent invitations by the user

    received_invitations = Invite.objects.filter(recipient=current_user, status='pending')


    context = {
        'sent_invitations': sent_invitations,
        'received_invitations': received_invitations,
        'user' : current_user,
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

            # Create a new Invite instance
            invite = Invite(sender=sender, recipient=user, team=team, status=status)

            # Save the invitation to the database
            invite.save()

            # Optionally, send notifications or emails to the recipient

            # Redirect to a success page or back to the dashboard
            return redirect('dashboard')

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


@login_required()
def create_team_view(request):
    """Display the team creation screen and handles team creations."""

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})

