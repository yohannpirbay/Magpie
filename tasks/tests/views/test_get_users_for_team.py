# tasks/tests/views/test_get_users_for_team.py

from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import User, Team

class GetUsersForTeamViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username='testuser')

        # Create a team and add the user as a member
        self.team = Team.objects.create(name='Test Team', description='Test Description')
        self.team.members.add(self.user)

    def test_get_users_for_existing_team(self):
        url = reverse('get_users_for_team', args=[self.team.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username.encode(), response.content)

    def test_get_users_for_nonexistent_team(self):
        # Get the URL for a nonexistent team's members
        url = reverse('get_users_for_team', args=[999])

        # Use the Django test client to make a GET request
        response = self.client.get(url, HTTP_ACCEPT='application/json')

        # Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)
