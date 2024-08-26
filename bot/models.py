from django.db import models
from accounts.models import BotUser
from django.contrib.auth.models import User


class Balance(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    amount = models.FloatField(default=0)


    def __str__(self):
        return f"{self.user.username} has {self.amount} ETB in wallet"





class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"