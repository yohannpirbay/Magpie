from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import Team

class TeamModelTestCase(TestCase):
    """Unit tests for the Team model."""

    fixtures = [
        'tasks/tests/fixtures/default_teams.json'
    ]


    def setUp(self):
        self.team = Team.objects.get(name='BronzeBulls')

    def test_valid_team(self):
        self._assert_team_is_valid()

    def test_team_name_cannot_be_blank(self):
        self.team.name = ''
        self._assert_team_is_invalid()

    def test_team_name_can_be_50_characters_long(self):
        self.team.name = 'x' * 50
        self._assert_team_is_valid()
    
    def test_team_name_cannot_be_over_50_characters_long(self):
        self.team.name = 'x' * 51
        self._assert_team_is_invalid()
    
    def test_team_description_cannot_be_blank(self):
        self.team.description = ''
        self._assert_team_is_invalid()

    def test_team_description_can_be_500_characters_long(self):
        self.team.description = 'x' * 500
        self._assert_team_is_valid()
    
    def test_team_description_cannot_be_over_500_characters_long(self):
        self.team.description = 'x' * 501
        self._assert_team_is_invalid()
    

    def _assert_team_is_valid(self):
        try:
            self.team.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_team_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.team.full_clean()

    
