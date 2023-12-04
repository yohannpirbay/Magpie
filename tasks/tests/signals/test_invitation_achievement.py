from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from tasks.models import Achievement, Notification, Team
from tasks.forms import InvitationForm
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.test import Client


class InvitationAchievementTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword', email='test@example.com',
            first_name='Test', last_name='User'
        )
        self.factory = RequestFactory()
        self.client = Client()

    def test_invitation_achievement(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Check if the user initially has no achievements
        self.assertEqual(self.user.achievements.count(), 0)

        # Create another user
        invited_user = get_user_model().objects.create_user(
            username='inviteduser', password='testpassword', email='invited@example.com',
            first_name='Invited', last_name='User'
        )

        # Create a team
        team = Team.objects.create(name='Test Team', description='Test Team Description')

        # Create an invitation (assuming you have a URL named 'send_invitation')
        form_data = {
            'user': invited_user.id,
            'team': team.id,
        }


        form = InvitationForm(form_data, user=self.user)

        reverse_url = reverse_lazy('send_invitation', kwargs={'user_id': self.user.id})
        csrf_token = self.client.get(reverse_url).cookies['csrftoken']

        request = self.factory.post(reverse_url, form_data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = self.client.post(
            reverse('send_invitation', kwargs={'user_id': self.user.id}), form_data, follow=True, HTTP_X_CSRFTOKEN=csrf_token)

        # Check if the invitation was sent successfully (status code 200 for a successful view response)
        self.assertEqual(response.status_code, 200)

        # Fetch the user after the invitation is sent
        user = get_user_model().objects.get(username='testuser')

        # Check if the achievement is added
        self.assertEqual(user.achievements.count(), 1)

        # Check if the notification is created
        notification = Notification.objects.get(user=user)
        self.assertEqual(
            notification.message, 'Congratulations! You earned the achievement: First Invitation'
        )
