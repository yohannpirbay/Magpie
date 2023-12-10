from django.test import TestCase
from django.urls import reverse
from tasks.models import Team, Invite, User

class InviteViewTests(TestCase):

    fixtures = [
        'tasks/tests/fixtures/default_teams.json'
    ]

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='email2@gmail.com')
        self.recipient_user = User.objects.create_user(username='recipient_user', password='password2', email='email1@gmail.com')
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
        response = self.client.post(reverse('send_invitation', args=[self.recipient_user.id]),{'user':self.recipient_user.id, 'team': 1})

        # Check if the invite is sent successfully
        self.assertRedirects(response, reverse('dashboard'), status_code=302)

        # Check if an invitation is created
        invite = Invite.objects.filter(sender=self.user, recipient=self.recipient_user).first()
        self.assertIsNotNone(invite)
