from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from tasks.forms import LogInForm, TeamForm
from tasks.models import User, Team
from tasks.tests.helpers import LogInTester, MenuTesterMixin, reverse_with_next

class LogInViewTestCase(TestCase, LogInTester, MenuTesterMixin):
    """Tests of the log in view."""
    """not finished yet"""

    fixtures = ['tasks/tests/fixtures/default_teams.json', 'tasks/tests/fixtures/default_user.json']

    def setUp(self):
        pass

    def test_create_team_url_with_redirect(self):
        pass

    def test_create_team_url_when_logged_in(self):
        pass

    def test_create_team_with_blank_name(self):
        pass

    def test_create_team_with_blank_description(self):
        pass

    def test_succesful_team_creation(self):
        pass

    def test_succesful_team_creation_with_redirect(self):
        pass

