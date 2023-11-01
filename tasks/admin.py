from django.contrib import admin
from .models import User  # Import your custom User model
from .models import Team, Invite

class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Users. """

    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'display_teams']

    def display_teams(self, obj):
        # Get the user's team memberships and concatenate the team names into a string
        team_names = ', '.join([team.name for team in obj.teams.all()])
        return team_names

    display_teams.short_description = 'Teams'  # Custom column name in admin interface

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']



# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
