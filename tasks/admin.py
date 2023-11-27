from django.contrib import admin
from .models import User, Team, Invite


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active', 'display_teams'
    ]

    def display_teams(self, obj):
        return ", ".join([team.name for team in obj.teams.all()])
    display_teams.short_description = 'Teams'

admin.site.register(User, UserAdmin)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for teams."""

    list_display = ['name', 'description', 'display_members']

    def display_members(self, obj):
        # Create a method to display members of each time as we can't directly display 'members'
        return ", ".join([member.username for member in obj.members.all()])

    # Change the name of the display column
    display_members.short_description = 'Members'
    
@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'team', 'status', )

