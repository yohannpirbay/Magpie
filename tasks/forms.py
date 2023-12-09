"""Forms for the tasks app."""
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError 
from .models import User, Team, Invite, Task




User = get_user_model()

# class InvitationForm(forms.Form):
#     user = forms.ModelChoiceField(queryset=User.objects.all(), label='Select User')
#     team = forms.ModelChoiceField(queryset=Team.objects.all(), label='Select Team')

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(InvitationForm, self).__init__(*args, **kwargs)

#     def clean_user(self):
#         user = self.cleaned_data.get('user')
#         if user == self.user:
#             raise ValidationError("You cannot send an invitation to yourself.")
#         return user
    
    


class InvitationForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='Select User')
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label='Select Team')

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('user', None)
        super(InvitationForm, self).__init__(*args, **kwargs)

    def clean_user(self):
        user = self.cleaned_data.get('user')

        # Check if an invitation has already been sent to the selected user
        if Invite.objects.filter(sender=self.sender, recipient=user).exists():
            raise ValidationError("An invitation has already been sent to this user.")

        # Check if the selected user is the sender
        if user == self.sender:
            raise ValidationError("You cannot send an invitation to yourself.")

        return user




    
class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user
    



class TeamForm(forms.ModelForm):
    """Form to create a team."""

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),  # Use CheckboxSelectMultiple for multiple selections
    )

    class Meta:
        """Form options."""
        model = Team
        fields = ['name', 'description', 'members']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.creator = user
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_user', 'due_date', 'team']