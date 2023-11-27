
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Achievement, Invite, Notification

@receiver(post_save, sender=get_user_model())
def team_created_achievement(sender, instance, created, **kwargs):
    # Your signal logic here
    pass

@receiver(post_save, sender=Invite)
def invitation_sent_achievement(sender, instance, created, **kwargs):
    # Your signal logic here
    pass
