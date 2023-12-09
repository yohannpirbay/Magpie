"""Unit tests of the task form."""
from django import forms
from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import User,Task,Team

class TaskFormTestCase(TestCase):
    """Unit tests of the task form."""

    def setUp(self):
        self.team = Team.objects.create(
            name = 'BronzeBulls',
            description = 'We are the bulls'
        )
        self.form_input = {
            'title': 'Task1',
            'description': 'Build the system',
            'assignedUsername': '@johndoe',
            'dueDate': '2032-12-25',
            'team': self.team
        }
        self.user = User.objects.create(
            username = "@johndoe",
            first_name = "Test",
            last_name = "User",
            email = "test@example.com"
        )

    def test_valid_task_form(self):
        form = TaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_task_form(self):
        form_data = self.form_input.copy()
        form_data['assignedUsername'] = "@thisUsernameDoesNotExist"
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_clean_dueDate(self):
        self.form_input['dueDate'] = '2015-10-21'
        form = TaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = TaskForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('assignedUsername', form.fields)
        self.assertIn('dueDate', form.fields)
        self.assertIn('team', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['assignedUsername'] = 'badusername'
        form = TaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        # Set the 'assignedUsername' to a valid username from the existing user
        self.form_input['assignedUsername'] = self.user.username
        
        form = TaskForm(data=self.form_input)
        before_count = Task.objects.count()
        
        if form.is_valid():
            form.save()
        
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)
        
        task = Task.objects.get(assignedUsername=self.user.username)  # Use the correct field for lookup
        self.assertEqual(task.title, 'Task1')
        self.assertEqual(task.description, 'Build the system')
        self.assertEqual(str(task.dueDate), '2032-12-25')
        self.assertEqual(task.team, self.team)

