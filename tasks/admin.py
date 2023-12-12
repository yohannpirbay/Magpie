from django.contrib import admin
from .models import User, Team, Invite


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Achievement,Task

class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active', 'display_teams', 'display_achievements',
        'display_sent_invites', 'display_received_invites' ,'id'
    ]

    def display_teams(self, obj):
        return ", ".join([team.name for team in obj.teams.all()])
    display_teams.short_description = 'Teams'

    def display_achievements(self, obj):
        return ", ".join([achievement.name for achievement in obj.achievements.all()])
    display_achievements.short_description = 'Achievements'

    def display_sent_invites(self, obj):
        return ", ".join([invite.recipient.username for invite in obj.sent_invites.all()])
    display_sent_invites.short_description = 'Sent Invites'

    def display_received_invites(self, obj):
        return ", ".join([invite.sender.username for invite in obj.received_invites.all()])
    display_received_invites.short_description = 'Received Invites'

admin.site.register(User, UserAdmin)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for teams."""

    list_display = ['name', 'description', 'display_members',]

    def display_members(self, obj):
        # Create a method to display members of each time as we can't directly display 'members'
        return ", ".join([member.username for member in obj.members.all()])

    # Change the name of the display column
    display_members.short_description = 'Members'
    
@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'team', 'status', )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'team', 'id','assigned_users_list', 'is_finished', 'finished_on']

    def assigned_users_list(self, obj):
        return ", ".join([user.username for user in obj.assigned_users.all()])

    assigned_users_list.short_description = 'Assigned Users'




