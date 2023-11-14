from django.core.management.base import BaseCommand
from tasks.models import Team

class Command(BaseCommand):
    help = 'Seed 10 teams'

    def handle(self, *args, **options):
        # Seed 100 teams
        for i in range(1, 11):
            team_name = f'Team {i}'
            Team.objects.get_or_create(name=team_name)

        self.stdout.write(self.style.SUCCESS('10 teams were seeded successfully.'))
