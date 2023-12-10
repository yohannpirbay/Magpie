# Assuming the imports are already present
from django import forms
from django.test import TestCase
from django.utils import timezone
from tasks.models import Task, Team, User
from tasks.forms import TaskForm  # Adjust the import based on your project structure

class TaskFormTestCase(TestCase):
    """Unit tests for the TaskForm."""

    fixtures = [
        'tasks/tests/fixtures/default_teams.json',
        'tasks/tests/fixtures/other_users.json',  # Update the fixture path
    ] 

    def setUp(self):
        self.team = Team.objects.get(name='BronzeBulls')
        self.user = User.objects.get(username='@janedoe')  # Assuming this username exists in your fixture

    def test_valid_task_form(self):
        form_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'assigned_user': self.user.id,
            'due_date': timezone.now().date() + timezone.timedelta(days=1),
            'team': self.team.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_due_date_in_the_past(self):
        form_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'assigned_user': self.user.id,
            'due_date': timezone.now().date() - timezone.timedelta(days=1),
            'team': self.team.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)
        self.assertEqual(form.errors['due_date'], ['Due date must be in the future.'])
