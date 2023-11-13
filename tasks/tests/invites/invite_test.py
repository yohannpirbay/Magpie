from django.test import TestCase
from django.contrib.auth.models import User
from .models import Team, Invite

class InviteTest(TestCase):
    def setUp(self):
        # Create two users for testing
        self.sender_user = User.objects.create_user(username='sender_user', password='password1')
        self.recipient_user = User.objects.create_user(username='recipient_user', password='password2')

        # Create a team
        self.team = Team.objects.create(name='Team A')

    def test_create_invite(self):
        # Create an invite
        invite = Invite.objects.create(
            sender=self.sender_user,
            recipient=self.recipient_user,
            team=self.team,
            status='pending'
        )

        # Check if the invite was created successfully
        self.assertEqual(invite.sender, self.sender_user)
        self.assertEqual(invite.recipient, self.recipient_user)
        self.assertEqual(invite.team, self.team)
        self.assertEqual(invite.status, 'pending')

    def test_accept_invite(self):
        # Create an invite
        invite = Invite.objects.create(
            sender=self.sender_user,
            recipient=self.recipient_user,
            team=self.team,
            status='pending'
        )

        # Simulate the recipient accepting the invite
        invite.status = 'accepted'
        invite.save()

        # Check if the invite status is updated to 'accepted'
        self.assertEqual(invite.status, 'accepted')

    def test_decline_invite(self):
        # Create an invite
        invite = Invite.objects.create(
            sender=self.sender_user,
            recipient=self.recipient_user,
            team=self.team,
            status='pending'
        )

        # Simulate the recipient declining the invite
        invite.status = 'declined'
        invite.save()

        # Check if the invite status is updated to 'declined'
        self.assertEqual(invite.status, 'declined')
