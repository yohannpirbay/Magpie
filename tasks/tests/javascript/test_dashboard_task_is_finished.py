from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from unittest.mock import patch
from tasks.models import Task, Team
from django.utils import timezone
from django.core.exceptions import SuspiciousOperation


class MarkAsFinishedTestCase(TestCase):
    def setUp(self):
        # Create a team
        self.team = Team.objects.create(name="Test Team")

        # Create a task with the associated team
        self.task = Task.objects.create(
            title="Test Task",
            description="Task description",
            due_date=timezone.now(),
            team=self.team
        )

    @patch('tasks.views.timezone.now')
    def test_mark_as_finished_view(self, mock_now):
        mock_now.return_value = timezone.now()
        
        # Ensure the task is not finished initially
        self.assertFalse(self.task.is_finished)

        # Make an AJAX request to mark the task as finished
        response = self.client.post(reverse('update_task_status', args=[self.task.id]), {'is_finished': True})

        # Check if the response is a JSON response
        self.assertIsInstance(response, JsonResponse)

        # Check if the 'error' key is present in the JSON response
        self.assertIn('error', response.json())

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Reload the task from the database (if needed)

        # Check if the task is not marked as finished on the server (if needed)
        self.assertFalse(self.task.is_finished)

    def test_mark_as_finished_view_with_invalid_task_id(self):
        # Make a non-AJAX request with an invalid task ID
        response = self.client.post(reverse('update_task_status', args=[999]), {'is_finished': True})

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Check if the 'error' key is present in the JSON response
        self.assertIn('error', response.json())

        # Check if the error message indicates that only AJAX requests are accepted
        self.assertIn('This endpoint only accepts AJAX requests.', response.json()['error'])