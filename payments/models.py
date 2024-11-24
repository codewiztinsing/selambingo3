from django.db import models
from accounts.models import TelegramUser

NULL = {"null": True, "blank": True}


class ChapaTransaction(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    pay_url = models.URLField()
    charge_price = models.FloatField(default=0)
    amount = models.BigIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    reference_no = models.CharField(max_length=100, **NULL)
    tx_ref = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.user}" + f"{self.amount}"
 
