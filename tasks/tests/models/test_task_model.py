"""Unit tests for the Task model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import Task, Team, User

class TaskModelTestCase(TestCase):
    """Unit tests for the Task model."""

    fixtures = [
        'tasks/tests/fixtures/default_teams.json',
        'tasks/tests/fixtures/default_tasks.json',
    ]

    def setUp(self):
        self.team = Team.objects.get(name = 'BronzeBulls')
        self.task = Task.objects.get(assignedUsername='@johndoe')
        self.task.team = self.team

    def test_valid_task(self):
        self._assert_task_is_valid()

    
    def test_title_cannot_be_blank(self):
        self.task.title = ''
        self._assert_task_is_invalid()

    def test_title_can_be_15_characters_long(self):
        self.task.title = '@' + 'x' * 14
        self._assert_task_is_valid()

    def test_title_cannot_be_over_15_characters_long(self):
        self.task.title = '@' + 'x' * 15
        self._assert_task_is_invalid()

    def test_title_is_not_unique(self):
        second_task = Task.objects.get(assignedUsername='@thisEmailInvalid')
        self.task.title = second_task.title
        self._assert_task_is_valid()

    
    def test_description_can_be_120_characters_long(self):
        self.task.description = '@' + 'x' * 119
        self._assert_task_is_valid()
    
    def test_description_cannot_be_over_120_characters_long(self):
        self.task.description = '@' + 'x' * 120
        self._assert_task_is_invalid()

    def test_description_cannot_be_blank(self):
        self.task.description = ''
        self._assert_task_is_invalid()

    
    def test_assignedUsername_can_be_30_characters_long(self):
        self.task.assignedUsername = '@' + 'x' * 29
        self._assert_task_is_valid()
    
    def test_assignedUsername_cannot_be_over_30_characters_long(self):
        self.task.assignedUsername = '@' + 'x' * 30
        self._assert_task_is_invalid()

    def test_assignedUsername_cannot_be_blank(self):
        self.task.assignedUsername = ''
        self._assert_task_is_invalid()

    def test_assignedUsername_is_not_unique(self):
        second_task = Task.objects.get(assignedUsername='@thisEmailInvalid')
        self.task.assignedUsername = second_task.assignedUsername
        self._assert_task_is_valid()

    def test_assignedUsername_must_start_with_at_symbol(self):
        self.task.assignedUsername = 'johndoe'
        self._assert_task_is_invalid()

    def test_assignedUsername_must_contain_only_alphanumericals_after_at(self):
        self.task.assignedUsername = '@john!doe'
        self._assert_task_is_invalid()

    def test_assignedUsername_must_contain_at_least_3_alphanumericals_after_at(self):
        self.task.assignedUsername = '@jo'
        self._assert_task_is_invalid()
    
    def test_assignedUsername_may_contain_numbers(self):
        self.task.assignedUsername = '@j0hndoe2'
        self._assert_task_is_valid()

    def test_assignedUsername_must_contain_only_one_at(self):
        self.task.assignedUsername = '@@johndoe'
        self._assert_task_is_invalid()


    def test_dueDate_cannot_be_blank(self):
        self.task.dueDate = ''
        self._assert_task_is_invalid()

    def test_dueDate_default_value(self):
        taskModel = Task.objects.create(
            title='Test Title',
            description='Test Description',
            assignedUsername='@testUser'
        )
        self.assertEqual(str(taskModel.dueDate), "2032-12-25")

    def test_team_can_be_null(self):
        self.task.team = None
        self._assert_task_is_valid()

    def test_team_can_be_blank(self):
        self.task = Task(
        title='TaskwithoutTeam',
        description='This task is not associated with any team',
        assignedUsername='@user',
        dueDate='2032-12-25',
        )
        self._assert_task_is_valid()

    def test_invalid_team_assignment(self):
        #this id doesn't exist in the database
        self.task.team_id = 999
        self._assert_task_is_invalid()

    def test_cascade_deletion_of_tasks(self):
        self.team.delete()
        deletedTask = Task.objects.filter(pk = self.task.pk).first()
        self.assertIsNone(deletedTask)

    def _assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_task_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.task.full_clean()