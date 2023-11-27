from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

#models.py

class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    achievement = models.ForeignKey('Achievement', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Achievement(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

class Team(models.Model):
    name = models.CharField(max_length=50, blank=False)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_teams', default=1)
    members = models.ManyToManyField('User', related_name='teams_joined')
    description = models.TextField(max_length=500, blank=False)  # Specify the default value as an empty string
    # Add a signal to trigger the achievement when a team is created
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.creator.achievements.add(Achievement.objects.get(name="First Team Created"))



class User(AbstractUser):
    """Model used for user authentication and team member-related information."""
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    teams = models.ManyToManyField(
        Team, related_name='memberships', blank=True)
    achievements = models.ManyToManyField('Achievement', blank=True)
    # Add these fields
    sent_invites = models.ManyToManyField('Invite', related_name='sent_invites', blank=True)
    received_invites = models.ManyToManyField('Invite', related_name='received_invites', blank=True)

    class Meta:
        """Model options."""
        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)

    def get_teams(self):
        return self.teams.all()

    def add_team(self, team):
        self.teams.add(team)


class Invite(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations', default=None)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations', default=None)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')), default=None)
    