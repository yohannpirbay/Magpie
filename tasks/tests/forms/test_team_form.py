from django import forms
from django.test import TestCase
from tasks.forms import TeamForm
from tasks.models import User, Team

class TeamFormTestCase(TestCase):
    """Unit tests of the team form."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.form_input = {
            'name': 'Test Team',
            'description': 'This is a test team.',
            'members': [1]
        }

    def test_form_has_required_fields(self):
        form = TeamForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('members', form.fields)

    def test_accepts_valid_input(self):
        form = TeamForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_requires_team_name(self):
        self.form_input['name'] = ''
        form = TeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_requires_team_description(self):
        self.form_input['description'] = ''
        form = TeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_form_requires_team_members(self):
        self.form_input['members'] = ''
        form = TeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('members', form.errors)
     

