from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the Profile model."""
    list_display = ('user', 'get_email', 'has_avatar')
    search_fields = ('user__username', 'user__email', 'bio')
    list_filter = ('user__is_active',)

    def get_email(self, obj):
        """Get the email of the associated user."""
        return obj.user.email
    get_email.short_description = _('Email')

    def has_avatar(self, obj):
        """Check if the profile has an avatar."""
        return bool(obj.avatar)
    has_avatar.boolean = True
    has_avatar.short_description = _('Has Avatar')
