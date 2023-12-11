from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from tasks.models import Task,User,Team
from datetime import datetime, timedelta

class UpdateTaskStatusTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        user = User.objects.create(username='test_user')

        # Create a team for testing with the user as a member
        team = Team.objects.create(
            name='Test Team',
            description='Test Team Description',
        )
        team.members.add(user)

        # Create a task for testing with a due date, assigned user, and team
        due_date = timezone.now() + timedelta(days=7)
        self.task = Task.objects.create(
            title='Test Task',
            is_finished=False,
            due_date=due_date,
            assigned_user=user,
            team=team,
        )

    def test_update_task_status(self):
        # Get the initial values
        initial_is_finished = self.task.is_finished
        initial_finished_on = self.task.finished_on

        # Simulate a request to update the task status
        response = self.client.post(reverse('update_task_status', args=[self.task.id]))

        # Reload the task from the database to get the updated values
        updated_task = Task.objects.get(id=self.task.id)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        # Check if the task status is updated
        self.assertNotEqual(initial_is_finished, updated_task.is_finished)
        # Check if finished_on is set to a datetime object
        self.assertIsNotNone(updated_task.finished_on)

        # Check if initial_finished_on is not None before comparing
        if initial_finished_on is not None:
            self.assertGreaterEqual(updated_task.finished_on, initial_finished_on)
