from django.core.management.base import BaseCommand, CommandError
from tasks.models import User, Team, Task, Invite

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
     # Query all users except the user with username "admin"
        deleted_user_count = User.objects.all().count()
        deleted_teams_count = Team.objects.all().count()
        deleted_tasks_count = Task.objects.all().count()
        deleted_invites_count = Invite.objects.all().count()
        User.objects.all().delete()
        Team.objects.all().delete()
        Task.objects.all().delete()
        Invite.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully unseeded {deleted_user_count} users, {deleted_teams_count} teams, {deleted_tasks_count} tasks, and {deleted_invites_count} invites.'))