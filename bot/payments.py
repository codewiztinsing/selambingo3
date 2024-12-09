from accounts.models import TelegramUser



def get_wallet_balance(user_id: int) -> float:
    """
    Get user's wallet balance from database
    
    Args:
        user_id (int): Telegram user ID
        
    Returns:
        float: User's current balance, or None if user not found
    """
    try:
        from .models import Wallet
        user = TelegramUser.objects.filter(telegram_id=user_id).first()
        wallet = Wallet.objects.filter(use=user).first()
        if wallet:
            return wallet.balance
        return None
    except Exception as e:
        print(f"Error getting wallet balance: {e}")
        return None
