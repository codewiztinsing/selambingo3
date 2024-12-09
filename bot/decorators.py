from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from payments import get_wallet_balance

def wallet_decorator(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        balance = get_wallet_balance(user_id)
        
        if balance is None:
            await update.message.reply_text("Please register first to play games!")
            return
            
        if balance <= 0:
            await update.message.reply_text("Insufficient balance! Please deposit to play.")
            return
            
        return await func(update, context, *args, **kwargs)
        
    return wrapper
