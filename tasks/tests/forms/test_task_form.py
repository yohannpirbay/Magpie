# In your tests.py file

from django.test import TestCase
from tasks.models import User
from tasks.forms import TaskForm
from datetime import datetime, timedelta
from tasks.models import Team

class TaskFormTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create teams for testing
        self.team1 = Team.objects.create(name='Team 1')
        self.team2 = Team.objects.create(name='Team 2')

        # Add the user to team1
        self.team1.members.add(self.user)

    def test_task_form_valid(self):
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'team': self.team1.id,  # Choosing the team before the user
            'assigned_user': self.user.id,
            'due_date': (datetime.now() + timedelta(days=7)).date(),  # Future date
        }

        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)



    def test_task_form_invalid_team_not_chosen(self):
        # Omit the team from the form data
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'assigned_user': self.user.id,
            'due_date': (datetime.now() + timedelta(days=7)).date(),  # Future date
        }

        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('team', form.errors)
