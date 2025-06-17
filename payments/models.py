from accounts.models import TelegramUser
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, related_name='wallet')
    balance = models.FloatField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class WinTracker(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='win_tracker')
    game_id = models.CharField(max_length=255)
    win_amount = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f"{self.user.username}'s Win Tracker"

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


class Charge(models.Model):
    game_id = models.CharField(max_length=255)
    betAmount = models.FloatField(default=0.00)
    player = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='charges')
    charged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.username}   {'charged' if self.charged else 'not charged'} for game {self.game_id}"
    


class PaymentSession(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=255,choices=[('PENDING','PENDING'),('SUCCESS','SUCCESS'),('FAILED','FAILED')])
    session_id = models.CharField(max_length=255,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reference_no = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} ({self.session_id})"  



class DepositMessage(models.Model):
    message = models.TextField()
    amount = models.FloatField(default=0.00)
    transaction_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_number} - {self.amount}"


class DepositedUser(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
