from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from tasks.models import Achievement, Notification, Team
from tasks.forms import TeamForm
from django.db import transaction

class TeamCreationAchievementTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword', email='test@example.com',
            first_name='Test', last_name='User'
        )
        self.factory = RequestFactory()
        self.client = Client()

    def test_team_creation_achievement(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Check if the user initially has no achievements
        self.assertEqual(self.user.achievements.count(), 0)

        # Create a team (assuming you have a URL named 'create_team')
        form_data = {
            'name': 'Test Team',
            'description': 'Test Team Description',
            'members': [self.user.id],  # assuming you have the user's ID
        }

        form = TeamForm(form_data)



        # Simulate the view by making a POST request
        csrf_token = self.client.get(
            reverse('create_team')).cookies['csrftoken']

        response = self.client.post(
            reverse('create_team'), form_data, follow=True, HTTP_X_CSRFTOKEN=csrf_token)

        # Check if the team creation was successful (status code 200 for a successful view response)
        self.assertEqual(response.status_code, 200)

        # Fetch the user after the team is created
        user = get_user_model().objects.get(username='testuser')

        # Check if the achievement is added
        self.assertEqual(user.achievements.count(), 1)

        # Check if the notification is created
        notification = Notification.objects.get(user=user)
        self.assertEqual(
            notification.message, 'Congratulations! You earned the achievement: First Team Created'
        )


        # Additional debugging for form validation and exceptions
        form = TeamForm(form_data)

        if form.is_valid():

            try:
                # Your team creation code here
                pass
            except Exception as e:
                print(f"Exception during team creation: {e}")
        else:
           
            print("Form errors:", form.errors)
