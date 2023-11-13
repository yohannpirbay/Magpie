from django.core.management.base import BaseCommand, CommandError
from tasks.models import User

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
     # Query all users except the user with username "admin"
        users_to_delete = User.objects.exclude(username='@admin')
        deleted_count = users_to_delete.count()
        users_to_delete.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully unseeded {deleted_count} users, except "super user @admin".'))