
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import TelegramUser
from .models import Wallet,PaymentSession

@receiver(post_save, sender=TelegramUser)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=0.00)





# @receiver(post_save, sender=PaymentSession)
# def update_wallet(sender, instance, created, **kwargs):
#     print("instance = ",instance)
#     print("created = ",created)
#     if created:
#         if instance.status == "paid":
#             wallet = Wallet.objects.get(user=instance.user)
#             wallet.balance += float(instance.amount)
#         wallet.save()
