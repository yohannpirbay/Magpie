# In your tests.py file

from django.test import TestCase
from tasks.models import Task, Team, User

class TaskModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a team for testing
        self.team = Team.objects.create(name='Test Team')

    def test_create_task(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            assigned_user=self.user,
            due_date="2023-12-31",  # Assuming a future date
            team=self.team
        )

        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task.")
        self.assertEqual(task.assigned_user, self.user)
        self.assertEqual(task.due_date, "2023-12-31")
        self.assertEqual(task.team, self.team)

