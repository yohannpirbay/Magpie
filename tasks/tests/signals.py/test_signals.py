# tasks/tests/test_signals.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import override_settings
from django.core.management import call_command
from tasks.models import Achievement, Notification, Invite
from tasks.signals import team_created_achievement, invitation_sent_achievement
from tasks.apps import TasksConfig  # Import your AppConfig

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SignalTests(TestCase):
    def setUp(self):
        # Run migrations before tests
        call_command('makemigrations', 'tasks')
        call_command('migrate')

    def test_team_created_achievement(self):
        # Call create_initial_achievements to ensure achievements are created
        TasksConfig.create_initial_achievements()

        user = get_user_model().objects.create(username='testuser', email='testuser@example.com')
        user.teams.create(name='Test Team')

        # Simulate the post_save signal
        team_created_achievement(sender=get_user_model(), instance=user, created=True)

        # Check if the achievement and notification are created
        print("\nChecking Team Created Achievement:")
        print("===================================")
        print("Does achievement 'First Team Created' exist in user?")
        if user.achievements.filter(name="First Team Created").exists():
            print("Yes, achievements:")
            print(user.achievements.all())
        else:
            print("No, achievements:")
            print(user.achievements.all())

        print("\nDoes notification for 'First Team Created' exist?")
        if Notification.objects.filter(user=user, message__contains="First Team Created").exists():
            print("Yes, notifications:")
            print(Notification.objects.all())
        else:
            print("No, notifications:")
            print(Notification.objects.all())

    def test_invitation_sent_achievement(self):
        # Call create_initial_achievements to ensure achievements are created
        print("\nTest: Invitation Sent Achievement")
        TasksConfig.create_initial_achievements()

        inviter = get_user_model().objects.create(username='inviter', email='inviter@example.com')
        invitee = get_user_model().objects.create(username='invitee', email='invitee@example.com')

        invite = Invite.objects.create(sender=inviter, recipient=invitee, team=inviter.teams.create(name='Test Team'), status='pending')

        # Simulate the post_save signal
        invitation_sent_achievement(sender=Invite, instance=invite, created=True)

        # Check if the achievement and notification are created for the sender
        print("\nChecking Invitation Sent Achievement:")
        print("===================================")
        print("Does achievement 'First Invitation' exist in inviter?")
        if inviter.achievements.filter(name="First Invitation").exists():
            print("Yes, achievements:")
            print(inviter.achievements.all())
        else:
            print("No, achievements:")
            print(inviter.achievements.all())

        print("\nDoes notification for 'First Invitation' exist?")
        if Notification.objects.filter(user=inviter, message__contains="First Invitation").exists():
            print("Yes, notifications:")
            print(Notification.objects.all())
        else:
            print("No, notifications:")
            print(Notification.objects.all())
