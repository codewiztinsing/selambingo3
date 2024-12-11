from accounts.models import TelegramUser
from django.db import models
class Wallet(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, related_name='wallet')
    balance = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"