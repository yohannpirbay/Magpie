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

    def test_get_users_for_team(self):
        # Get the URL for the team's members
        url = reverse('get_users_for_team', args=[self.team.id])

        # Use the Django test client to make a GET request
        response = self.client.get(url, HTTP_ACCEPT='application/json')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response data contains the user's information
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.user.id)
        self.assertEqual(data[0]['username'], self.user.username)

    def test_get_users_for_nonexistent_team(self):
        # Get the URL for a nonexistent team's members
        url = reverse('get_users_for_team', args=[999])

        # Use the Django test client to make a GET request
        response = self.client.get(url, HTTP_ACCEPT='application/json')

        # Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Check that the response data is empty
        data = response.json()
        self.assertEqual(len(data), 0)
