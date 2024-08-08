from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class BotUser(AbstractBaseUser):
    username = models.CharField(_('username'), max_length=30, unique=True)
    phone    = models.CharField(_('phone'), max_length=20, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name        = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Return the username.
        """
        return self.username

    def get_short_name(self):
        """Return the username."""
        return self.username