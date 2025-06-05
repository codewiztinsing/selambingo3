from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

BACK_URL = "https://api.selambingo.com"

async def handle_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle deposits from other payment methods
    """
    # Get amount from the query
    
    query = update.callback_query
    await query.edit_message_text("Please enter the amount you want to deposit:")  
 

  


    # Validate amount
    if amount <= 0:
        await update.message.reply_text("Please enter a valid amount greater than 0.")
        return ConversationHandler.END
    try:
        # Generate reference number
        user_id = update.effective_user.id
        username = update.effective_user.username
        amount = context.user_data['amount']
        reference_no = f"manual_deposit_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        checkout_url = "https://gateway.arifpay.org/api/checkout/session"

        payload = {
            "cancelUrl": "https://api.selambingo.com/",
            "phone":"0991221912",
            "email":"telebirrTest@gmail.com",
            "nonce": "AAAa123asds", 
            "errorUrl": "http://error.com",
            "notifyUrl": "https://api.selambingo.com/",
            "successUrl": "https://api.selambingo.com/",
            "paymentMethods":  ["TELEBIRR","AWASH","AWASH_WALLET","PSS","CBE","AMOLE","BOA","KACHA","TELEBIRR_USSD","HELLOCASH","MPESSA"],
            "expireDate": "2025-02-01T03:45:27",
            "items": [
                {
                    "name": "Selam bingo",
                    "quantity": 1,
                    "price": 12,
                    "description": "Selam bingo deposit",
                    "image": "https://4.imimg.com/data4/KK/KK/GLADMIN-/product-8789_bananas_golden-500x500.jpg"
                }
            ],
            "beneficiaries": [
                {
                    "accountNumber": "01320811436100", 
                    "bank": "AWINETAA",
                    "amount": amount
                }
            ],
            "lang": "EN"
        }

        headers = {
            "x-arifpay-key": "aXOIyscT4H6TO0yrR1V32ehuzXquwlux"
                    
        }
        print("headers",headers)

        response = requests.post(checkout_url, json=payload, headers=headers)
        print("response",response.json())
        if response.status_code == 200:
            print("response",response.json())
            session_id = response.json().get("data", {}).get("sessionId")
            return session_id
        return None
            
                


    

        
    except Exception as e:
        logger.error(f"Error handling manual deposit: {str(e)}")
        error_message = "Sorry, there was an error processing your request. Please try again later."
        if update.callback_query:
            await update.callback_query.edit_message_text(error_message)
        else:
            await update.message.reply_text(error_message)
        
    return ConversationHandler.END

