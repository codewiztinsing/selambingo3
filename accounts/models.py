from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class TelegramUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username