from django.core.management.base import BaseCommand
from your_app.models import Team

class Command(BaseCommand):
    help = 'Seed 100 teams'

    def handle(self, *args, **options):
        # Seed 100 teams
        for i in range(1, 101):
            team_name = f'Team {i}'
            Team.objects.get_or_create(name=team_name)

        self.stdout.write(self.style.SUCCESS('100 teams were seeded successfully.'))
