from django.core.management.base import BaseCommand
from your_app.models import Team

class Command(BaseCommand):
    help = 'Delete all teams'

    def handle(self, *args, **options):
        Team.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All teams were deleted.'))
