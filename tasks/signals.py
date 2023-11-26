from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Team, Invite, Achievement

@receiver(post_save, sender=Team)
def team_created_achievement(sender, instance, created, **kwargs):
    if created:
        instance.save()

@receiver(post_save, sender=Invite)
def invitation_sent_achievement(sender, instance, created, **kwargs):
    if created:
        instance.save()
