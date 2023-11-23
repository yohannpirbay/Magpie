from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class Team(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=500, blank=False)  # Specify the default value as an empty string
    members = models.ManyToManyField('User')


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
    
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignedUsername = models.ForeignKey(User, on_delete=models.CASCADE)
    dueDate = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
