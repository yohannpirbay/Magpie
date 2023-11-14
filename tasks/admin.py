from django.contrib import admin
from .models import User, Team, Invite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
    ]


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

