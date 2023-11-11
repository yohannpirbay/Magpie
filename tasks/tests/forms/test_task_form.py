"""Unit tests of the task form."""
from django import forms
from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import User,Task

class TaskFormTestCase(TestCase):
    """Unit tests of the task form."""

    def setUp(self):
        self.form_input = {
            'title': 'Task1',
            'description': 'Build the system',
            'assignedUsername': '@johndoe',
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

    def test_form_has_necessary_fields(self):
        form = TaskForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('assignedUsername', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['assignedUsername'] = 'badusername'
        form = TaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = TaskForm(data=self.form_input)
        before_count = Task.objects.count()
        if form.is_valid():
            form.save()
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count+1)
        task = Task.objects.get(assignedUsername='@johndoe')
        self.assertEqual(task.title, 'Task1')
        self.assertEqual(task.description, 'Build the system')

