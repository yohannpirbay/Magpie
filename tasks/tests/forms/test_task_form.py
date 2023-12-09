"""Unit tests of the task form."""
from django import forms
from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import User,Task,Team

class TaskFormTestCase(TestCase):
    """Unit tests of the task form."""

    def setUp(self):
        self.user = User.objects.create(username="johndoe", first_name="John", last_name="Doe",
                                        email="john@example.com")
        self.team = Team.objects.create(name='BronzeBulls', description='We are the bulls')

        self.form_input = {
            'title': 'Task1',
            'description': 'Build the system',
            'assigned_users': [self.user.id],  # Pass a list of user IDs
            'dueDate': '2032-12-25',
            'team': self.team.id  # Pass the team ID
        }

    def test_valid_task_form(self):
        form = TaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_task_form(self):
        form_data = self.form_input.copy()
        form_data['dueDate'] = '2000-01-01'  # Past date for invalid test
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
        self.assertIn('assigned_users', form.fields)
        self.assertIn('dueDate', form.fields)
        self.assertIn('team', form.fields)

    # def test_form_uses_model_validation(self):
    #     self.form_input['assignedUsername'] = 'badusername'
    #     form = TaskForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = TaskForm(data=self.form_input)
        before_count = Task.objects.count()
        if form.is_valid():
            task = form.save()
            self.assertIsNotNone(task.id)
            self.assertTrue(self.user in task.assigned_users.all())
            self.assertEqual(task.team.id, self.team.id)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)
        new_task = Task.objects.get(id=task.id)
        self.assertEqual(new_task.title, 'Task1')
        self.assertEqual(new_task.description, 'Build the system')
        self.assertEqual(new_task.dueDate.strftime('%Y-%m-%d'), '2032-12-25')
        self.assertTrue(self.user in new_task.assigned_users.all())
        self.assertEqual(new_task.team, self.team)
