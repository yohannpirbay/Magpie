from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import Team

class UpdateUsersTestCase(TestCase):

    def test_update_users_with_team(self):
        team = Team.objects.create(name="Test Team")
        response = self.client.get(reverse('get_users_for_team', args=[team.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_update_users_without_team(self):
        response = self.client.get(reverse('get_users_for_team', args=[1]))
        self.assertEqual(response.status_code, 404)
