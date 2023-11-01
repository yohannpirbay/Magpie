from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Users. """

    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active']

# Register your models here.
admin.site.register(User, UserAdmin)
