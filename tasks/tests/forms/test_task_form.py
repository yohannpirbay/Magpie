from django.test import TestCase
from django.utils import timezone
from tasks.forms import TaskForm
from tasks.models import Task, Team, User
from datetime import date

class TaskFormTestCase(TestCase):

    def setUp(self):
        # Create a team and a user for the form to use in the queryset
        self.team = Team.objects.create(name='Test Team', description='Test description')
        self.user = User.objects.create(username='testuser', password='testpassword')

    def test_valid_form(self):
        data = {
            'title': 'Test Task',
            'description': 'Test description',
            'assigned_user': self.user.id,
            'due_date': date.today() + timezone.timedelta(days=7),
            'team': self.team.id,
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_due_date_in_past(self):
        data = {
            'title': 'Test Task',
            'description': 'Test description',
            'assigned_user': self.user.id,
            'due_date': date.today() - timezone.timedelta(days=1),
            'team': self.team.id,
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Due date must be in the future.', form.errors['due_date'])
