from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    """
    User profile model that extends the built-in User model.
    Contains additional user information like bio and avatar.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )
    bio = models.TextField(
        verbose_name=_('Biography'),
        help_text=_('Tell something about yourself'),
        blank=True
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name=_('Profile Picture'),
        help_text=_('Upload your profile picture')
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"
