from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Invite, Team

class InvitesViewTest(TestCase):
    
    fixtures = ['tasks/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        
        self.team1 = Team.objects.create(name='Team 1')
        self.team2 = Team.objects.create(name='Team 2')

        # Create invitations for testing
        self.received_invitation = Invite.objects.create(
            recipient=self.user,
            sender=User.objects.create_user(username='@senderuser', password='Password123'),
            team=self.team1,
            status='pending'
        )
        self.sent_invitation = Invite.objects.create(
            recipient=User.objects.create_user(username='@recipientuser', password='Password123'),
            sender=self.user,
            team=self.team2,
            status='pending'
        )

    def test_invites_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('invites'))
        self.assertEqual(response.status_code, 200)

        # Check if received invitation information is present in the response
        self.assertContains(response, f'You {self.user.username} have been invited to join {self.received_invitation.team.name} by {self.received_invitation.sender.username}')

        # Check if sent invitation information is present in the response
        self.assertContains(response, f'You have sent an invitation to {self.sent_invitation.recipient.username} to join {self.sent_invitation.team.name}')