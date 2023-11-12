"""Unit tests of the team form."""
from django import forms
from django.test import TestCase
from tasks.forms import TeamForm, UserForm
from tasks.models import Team


class TeamFormTestCase(TestCase):
    """Unit tests of the team form."""

    fixtures = [
        'tasks/tests/fixtures/default_team.json'
    ]

    def setUp(self):
        self.user_form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
        }

        user_form = UserForm(data=self.user_form_input)
        self.user = user_form.save()

        self.team_form_input = {
            'name': 'Magpie',
            'description': 'SEG small group team',
            'members': [self.user]
        }

    def test_form_has_necessary_fields(self):
        form = TeamForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('members', form.fields)

    def test_valid_team_form(self):
        team_form = TeamForm(data=self.team_form_input)
        self.assertTrue(team_form.is_valid())

    def test_form_must_save_correctly(self):
        team = Team.objects.get(name='Test Team')
        form = TeamForm(instance=team, data=self.team_form_input)
        before_count = Team.objects.count()
        form.save()
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(team.name, 'Magpie')
        self.assertEqual(team.description, 'SEG small group team')

    def test_character_limit_team_form(self):
        long_name = 'A' * 51
        long_description = 'A' * 501
        self.team_form_input['name'] = long_name
        self.team_form_input['description'] = long_description
        form = TeamForm(data=self.team_form_input)
        self.assertEqual(form.errors['name'], ['Ensure this value has at most 50 characters (it has 51).'])
        self.assertEqual(form.errors['description'], ['Ensure this value has at most 500 characters (it has 501).'])

    def test_blank_team_form(self):
        self.team_form_input['name'] = ''
        self.team_form_input['description'] = ''
        self.team_form_input['members'] = []
        form = TeamForm(data=self.team_form_input)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['description'], ['This field is required.'])
        self.assertEqual(form.errors['members'], ['This field is required.'])

