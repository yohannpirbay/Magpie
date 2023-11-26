"""Tests of the dashboard view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Team, Task
from datetime import datetime

class DashboardViewTestCase(TestCase):

    fixtures = ['tasks/tests/fixtures/default_user.json',
                'tasks/tests/fixtures/default_teams.json',
                'tasks/tests/fixtures/default_tasks.json',]
    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(name = 'BronzeBulls')
        self.task = Task.objects.get(assignedUsername='@johndoe')
        self.task.team = self.team
        self.task2 = Task.objects.get(pk = 2)
        self.task2.team = self.team
        

    def test_dashboard_sorts_due_date_ascending(self):
        self.client.login(username=self.user.username, password="Password123")
        url = reverse('dashboard') + '?sort_order_due_date=ascending'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        due_dates = [datetime.strptime(str(task.dueDate), '%Y-%m-%d') for task in response.context['tasks']]
        self.assertListEqual(due_dates, sorted(due_dates))

    def test_dashboard_sorts_due_date_descending(self):
        self.client.login(username=self.user.username, password="Password123")
        url = reverse('dashboard') + '?sort_order_due_date=descending'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        due_dates = [datetime.strptime(str(task.dueDate), '%Y-%m-%d') for task in response.context['tasks']]
        self.assertListEqual(due_dates, sorted(due_dates, reverse= True))

