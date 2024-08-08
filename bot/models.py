from django.db import models
from accounts.models import BotUser
from django.contrib.auth.models import User


class Balance(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    amount = models.FloatField(default=0)


    def __str__(self):
        return f"{self.user.username} has {self.amount} ETB in wallet"
