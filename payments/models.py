from accounts.models import TelegramUser
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, related_name='wallet')
    balance = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Commission(models.Model):
    GAME_TYPES = [
        ('10', '10'),
        ('20', '20'),
        ('50', '50'),
        ('100', '100'),
    ]
    amount = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game_type = models.CharField(max_length=255, choices=GAME_TYPES)
    

    def __str__(self):
        return f" from {self.game_type} {self.amount} we get {self.amount} Commission"