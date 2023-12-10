from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from tasks.forms import LogInForm, TeamForm
from tasks.models import User, Team

class CreateTeamViewTestCase(TestCase):
    """Tests of the create team view"""
    """not finished yet"""

    fixtures = ['tasks/tests/fixtures/default_teams.json', 'tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_team')
        self.user = User.objects.get(username='@johndoe')

    def test_create_team_url_when_logged_out(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_team_url_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_team_with_blank_name(self):
        self.client.force_login(self.user)
        data = {'name': '', 'description': 'Team Description'}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'This field is required.')


    def test_create_team_with_blank_description(self):
        self.client.force_login(self.user)
        data = {'name': 'Team Name', 'description': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'description', 'This field is required.')

    def test_succesful_team_creation(self):
        self.client.force_login(self.user)
        data = {'name': 'Team Name', 'description': 'Team Description', 'members': self.user.id}
        response = self.client.post(self.url, data)
        print(response.content)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Team.objects.filter(name='Team Name').count(), 1)


