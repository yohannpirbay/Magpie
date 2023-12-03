from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Achievement, Notification, Invite

@receiver(post_save, sender=get_user_model())
def team_created_achievement(sender, instance, created, **kwargs):

    if created and instance.teams.exists():
        # Check if the user already has the "First Team Created" achievement
        if not instance.achievements.filter(name="First Team Created").exists():
            achievement, _ = Achievement.objects.get_or_create(name="First Team Created")
            instance.achievements.add(achievement)

            message = f"Congratulations! You earned the achievement: {achievement.name}"
            notification = Notification.objects.create(user=instance, message=message, achievement_id=achievement.id)

            #print(f"Notification created - ID: {notification.id}, User: {notification.user}, Message: {notification.message}, Achievement: {notification.achievement}, Created At: {notification.created_at}")


@receiver(post_save, sender=Invite)
def invitation_sent_achievement(sender, instance, created, **kwargs):
    
    if created:
     
        # Get the sender of the invite
        sender_user = instance.sender

        # Check if the sender already has the achievement
        achievement_name = "First Invitation"
        if not sender_user.achievements.filter(name=achievement_name).exists():
            achievement = Achievement.objects.get(name=achievement_name)

            # Add the achievement to the sender
            sender_user.achievements.add(achievement)

            # Trigger the notification with achievement ID
            message = f"Congratulations! You earned the achievement: {achievement.name}"
            notification = Notification.objects.create(user=sender_user, message=message, achievement_id=achievement.id)

            # Print the notification details    
            #print(f"Notification created - ID: {notification.id}, User: {notification.user}, Message: {notification.message}, Achievement: {notification.achievement}, Created At: {notification.created_at}")
