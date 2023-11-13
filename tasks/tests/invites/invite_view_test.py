from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Team, Invite

class InviteViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.team = Team.objects.create(name='Team 1')

    def test_accept_invite(self):
        # Create an invite
        invite = Invite.objects.create(sender=self.user, recipient=self.user, team=self.team, status='pending')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Accept the invitation
        response = self.client.get(reverse('accept_invite', args=[invite.id]))

        # Check if the invitation status is updated to 'accepted'
        invite.refresh_from_db()
        self.assertEqual(invite.status, 'accepted')

        # Check if the view redirects to the dashboard
        self.assertRedirects(response, reverse('dashboard'))

    def test_decline_invite(self):
        # Create an invite
        invite = Invite.objects.create(sender=self.user, recipient=self.user, team=self.team, status='pending')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Decline the invitation
        response = self.client.get(reverse('decline_invite', args=[invite.id]))

        # Check if the invitation status is updated to 'declined'
        invite.refresh_from_db()
        self.assertEqual(invite.status, 'declined')

        # Check if the view redirects to the dashboard
        self.assertRedirects(response, reverse('dashboard'))

    def test_send_invitation(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send an invitation to the test user
        response = self.client.post(reverse('send_invitation', args=[self.user.id]))

        # Check if the view redirects to the dashboard
        self.assertRedirects(response, reverse('dashboard'))

        # Check if an invitation is created
        invite = Invite.objects.filter(sender=self.user, recipient=self.user).first()
        self.assertIsNotNone(invite)
