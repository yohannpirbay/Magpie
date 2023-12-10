from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from tasks.forms import LogInForm
from tasks.models import User, Team, Task

class CreateTasksTestCase(TestCase):
    """Test of create tasks view"""

    def setUp(self):
        pass

    def test_create_task_url_when_logged_out(self):
        pass

    def test_create_task_url_when_logged_in(self):
        pass

    def test_create_task_with_blank_title(self):
        pass

    def test_create_task_with_blank_description(self):
        pass

    def test_succesful_task_creation(self):
        pass
