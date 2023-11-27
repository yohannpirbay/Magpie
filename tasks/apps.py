# tasks/apps.py
from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    
    def ready(self):
        # Import and connect signals in the ready method
        import tasks.signals  # This will import and connect your signals

        # Create achievements when the app is ready
        self.create_initial_achievements()

    def create_initial_achievements(self):
        from .models import Achievement

        # Check if achievements already exist
        if not Achievement.objects.exists():
            Achievement.objects.create(name="First Team Created", description="You created your first team!")
            Achievement.objects.create(name="First Invitation", description="You invited your first teammate!")
