from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes
# from telegram import filters  # Updated import for filters
import requests
import os
from decouple import config
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import requests
import logging
import re
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

BACK_URL = "https://api.selambingo.com/"
user_data = {}  
# Define states for conversation
PHONE,EMAIL,PASSWORD,CONFIRM_PASSWORD = range(4)

logger = logging.getLogger(__name__)

# Email validation regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'




def play_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🎮 Play 10", callback_data='10'),
         InlineKeyboardButton("🎮 Play 20", callback_data='20')],
        [InlineKeyboardButton("🎮 Play 50", callback_data='50'),
         InlineKeyboardButton("🎮 Play 100", callback_data='100')],
        [InlineKeyboardButton("🎮 Play Demo", callback_data='play_demo'),
         InlineKeyboardButton("🔙  Back to Menu", callback_data='back')
         ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    email = update.message.text

    await update.message.reply_text("Please Enter your Email:")

    # Initialize user data if it doesn't exist
    if user_id not in user_data:
        user_data[user_id] = {}  # Create a new entry for the user

    # Validate the email format
    if re.match(EMAIL_REGEX, email):
        user_data['email'] = email
        await update.message.reply_text("Thank you! Your email has been recorded. Please provide your password:")
        return PASSWORD  # Move to the next state (PASSWORD)
    else:
        await update.message.reply_text("Invalid email format. Please enter a valid email address:")
        return EMAIL  # Stay in the email state to allow re-entry


async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data['password'] = update.message.text

    await update.message.reply_text("Please confirm your password:")
    return CONFIRM_PASSWORD



async def begin_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referral_id = context.user_data.get('referral_id')
    print("referral_id",referral_id)

    if referral_id:
        print("referral_id",referral_id)
        user_data['referred_by'] = referral_id
        # Get referrer's telegram user info
        try:
            referrer_user = await context.bot.get_chat(int(referral_id))
            referrer_name = referrer_user.first_name
            user_data['referrer_name'] = referrer_name
            await update.message.reply_text(f"Welcome! You were invited by user {referrer_name}")
        except Exception as e:
            logger.error(f"Error getting referrer info: {e}")
            referrer_name = "unknown"
    else:
        print("no referral_id")

    user_id = update.message.from_user.id
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    user_data["username"] = username



    url  = f"{BACK_URL}/accounts/filter-users/{user_id}/"
    user_exists  = requests.get(url)
    if user_exists.status_code == 200:
        user_exists = user_exists.json()
        
        await update.message.reply_text(
                    text="You are already registred,please start playing:",
                    reply_markup=play_options_keyboard()
                )
    else:
        await update.message.reply_text(f"Welcome! Your username is: {username}. Please share your phone number.")
        # Create a button to share phone number
        phone_button = KeyboardButton("Share Phone Number", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[phone_button]], resize_keyboard=True, one_time_keyboard=True)

        await update.message.reply_text("Click the button below to share your phone number:", reply_markup=reply_markup)

        return PHONE  # Move to the PHONE state

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the message contains a contact
    if update.message.contact:
        # Check if user was referred and add bonus to referrer's wallet
        if 'referred_by' in user_data:
            try:
                # Add 5 ETB bonus to referrer's wallet
                referrer_bonus_data = {
                    'user_id': int(user_data['referred_by']),
                    'amount': 5
                }
                bonus_response = requests.post(f'{BACK_URL}/payments/add-balance/', 
                                            json=referrer_bonus_data)
                
                if bonus_response.status_code == 200:
                    referrer_name = user_data.get('referrer_name', 'your referrer')
                    await update.message.reply_text(f"Added 5 ETB bonus to {referrer_name}'s wallet!")
                else:
                    logger.error(f"Failed to add referral bonus: {bonus_response.text}")
            except Exception as e:
                logger.error(f"Error adding referral bonus: {e}")

      

        phone_number = update.message.contact.phone_number
        user_data["phone"] = phone_number

        user_id = update.message.from_user.id
        first_name = update.message.from_user.first_name,
        last_name = update.message.from_user.last_name
        confirm_password= update.message.text
        user_data.update({'password_confirm':confirm_password})
        user_data.update({
            'telegram_id': update.message.from_user.id
        })
        user_data.update({
            'phone': user_data.get('phone',"botphone")
        })

        username = user_data.get("username",first_name)
        phone = user_data.get('phone',"botphone")
        password = "123456"
        confirm_password ="123456"
        user_data.update({'password':password})
        user_data.update({'password_confirm':confirm_password})
        response = requests.post(f"{BACK_URL}/accounts/register/", data=user_data)
        

        if response.status_code == 201:  # Assume 201 means success
            await update.message.reply_text("Registration completed successfully!")
            await update.message.reply_text("Please click the button below to proceed to the next step:", reply_markup=play_options_keyboard())
        else:
        
            await update.message.reply_text(f"Registration failed")

      

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration canceled.")
    return ConversationHandler.END

