from django.core.management.base import BaseCommand
from accounts.models import TelegramUser

class Command(BaseCommand):
    help = 'Creates a superuser with telegram details'

    def handle(self, *args, **kwargs):
        username = input("Username: ")
        telegram_id = input("Telegram ID: ")
        password = input("Password: ")
        
        user = TelegramUser.objects.create_superuser(
            username=username,
            telegram_id=telegram_id,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}"'))