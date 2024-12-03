from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class TelegramUser(AbstractUser):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message=_('Enter a valid username. This value may contain only letters, '
                     'numbers, and @/./+/-/_ characters.')
        )]
    )
    telegram_id = models.BigIntegerField(_('Telegram ID'), unique=False)
    first_name = models.CharField(_('First Name'), max_length=64, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=64, blank=True)
    telegram_username = models.CharField(_('Telegram Username'), max_length=32, blank=True)
    phone = models.CharField(_('Phone'), max_length=32, blank=True)
    language_code = models.CharField(_('Language Code'), max_length=10, blank=True)
    is_bot = models.BooleanField(_('Is Bot'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)


    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='telegram_user_set',
        related_query_name='telegram_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='telegram_user_set',
        related_query_name='telegram_user'
    )

    


    def __str__(self):
        return f"{self.username} ({self.telegram_id})"
 
