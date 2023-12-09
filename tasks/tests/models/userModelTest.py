from django.test import TestCase
from tasks.models import User, Team

''' Unit test to check if users are assigned to teams correctly '''
class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username='testuser', email='testuser@example.com', password='testpassword')
        
        # Create some teams
        self.team1 = Team.objects.create(name='Team A')
        self.team2 = Team.objects.create(name='Team B')

        # Add the user to the teams
        self.user.teams.add(self.team1, self.team2)

    def test_get_teams(self):
        # Get the user's team memberships
        user_teams = self.user.get_teams()

        # Check if the user is a member of the expected teams
        self.assertEqual(user_teams.count(), 2)  # Check if the user is a member of two teams
        self.assertIn(self.team1, user_teams)
        self.assertIn(self.team2, user_teams)
