from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from tasks.forms import LogInForm
from tasks.models import User, Team, Task

class CreateTasksTestCase(TestCase):
    """Test of create tasks view"""

    fixtures = ['tasks/tests/fixtures/default_teams.json', 'tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_task')
        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(name='BronzeBulls')

    def test_create_task_url_when_logged_out(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_task_url_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_task_with_blank_title(self):
        self.client.force_login(self.user)
        data = {'title': '', 'description': 'Task Description'}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'title', 'This field is required.')


    def test_create_task_with_blank_description(self):
        self.client.force_login(self.user)
        data = {'title': 'New Task', 'description': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'description', 'This field is required.')

    def test_create_task_with_blank_user(self):
        self.client.force_login(self.user)
        data = {'title': 'New Task', 'description': 'New Description', 'assigned_user': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'assigned_user', 'This field is required.')

    def test_create_task_with_blank_due_date(self):
        self.client.force_login(self.user)
        data = {'title': 'New Task', 'description': 'New Description', 'assigned_user': self.user.id, 'due_date': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'due_date', 'This field is required.')

    def test_create_task_with_blank_team(self):
        self.client.force_login(self.user)
        data = {'title': 'New Task', 'description': 'New Description', 'assigned_user': self.user.id, 'due_date': '2024-02-29', 'team': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'team', 'This field is required.')

    def test_succesful_task_creation(self):
        self.client.force_login(self.user)
        data = {'title': 'New Task', 'description': 'New Description', 'assigned_user': self.user.id, 'due_date': '2024-02-29', 'team': self.team.id}
        response = self.client.post(self.url, data)
        print(response.content)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Task.objects.filter(title='New Task').count(), 1)
