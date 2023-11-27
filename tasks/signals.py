
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
        create_initial_achievements()
        achievement = Achievement.objects.get(name="First Team Created")
        instance.achievements.add(achievement)


        # Trigger the notification with achievement ID
        message = f"Congratulations! You earned the achievement: {achievement.name}"
        notification  = Notification.objects.create(user=instance, message=message, achievement_id=achievement.id)
        # Print the notification details
        
        print(f"Notification created - ID: {notification.id}, User: {notification.user}, Message: {notification.message}, Achievement: {notification.achievement}, Created At: {notification.created_at}")

@receiver(post_save, sender=Invite)
def invitation_sent_achievement(sender, instance, created, **kwargs):
    pass