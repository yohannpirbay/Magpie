
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Achievement, Invite, Notification

def create_initial_achievements():
    from .models import Achievement

        # Check if achievements already exist
    if not Achievement.objects.exists():
        Achievement.objects.create(name="First Team Created", description="You created your first team!")
        Achievement.objects.create(name="First Invitation", description="You invited your first teammate!")


@receiver(post_save, sender=get_user_model())
def team_created_achievement(sender, instance, created, **kwargs):
    pass
@receiver(post_save, sender=Invite)
def invitation_sent_achievement(sender, instance, created, **kwargs):
    pass