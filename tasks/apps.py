# tasks/apps.py
from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Importing models here to ensure that the app registry is ready
        from .models import Achievement

        # Create achievements when the app is ready
        self.create_initial_achievements()

    def create_initial_achievements(self):
        from .models import Achievement

        # Check if achievements already exist
        if not Achievement.objects.filter(name="First Team Created").exists():
            Achievement.objects.create(name="First Team Created", description="You created your first team!")

        if not Achievement.objects.filter(name="First Invitation").exists():
            Achievement.objects.create(name="First Invitation", description="You invited your first teammate!")

        if not Achievement.objects.filter(name="Fyoo").exists():
            Achievement.objects.create(name="Fyoo", description="You invited your first teammate!")
