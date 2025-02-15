from django.core.management.base import BaseCommand
from payments.models import Wallet, TelegramUser

class Command(BaseCommand):
    help = 'Reset all wallet balances to 0'

    def handle(self, *args, **options):
        try:
            # Get all wallets
            wallets = Wallet.objects.all()
            
            # Reset balance to 0 for each wallet
            updated_count = wallets.update(balance=0)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully reset {updated_count} wallet balances to 0')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error resetting wallets: {str(e)}')
            )
