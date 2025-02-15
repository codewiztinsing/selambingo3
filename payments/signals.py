
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import TelegramUser
from .models import Wallet,PaymentSession

@receiver(post_save, sender=TelegramUser)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=0.00)





