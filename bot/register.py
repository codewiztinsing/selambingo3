from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes
# from telegram import filters  # Updated import for filters
import requests
import os
from decouple import config
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import requests
import re
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

BACK_URL = config('BACK_URL')
user_data = {}  
# Define states for conversation
PHONE,EMAIL,PASSWORD,CONFIRM_PASSWORD = range(4)


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
    user_id = update.message.from_user.id
    username = update.message.from_user.username if update.message.from_user.username else "Not provided"
    user_data["username"] = username

    url  = f"{BACK_URL}/accounts/filter-users/?username={username}"
    user_exists  = requests.get(url).json()
    if len(user_exists) > 0:
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
        phone_number = update.message.contact.phone_number
        user_data["phone"] = phone_number
      
        
        await update.message.reply_text(f"Plase Enter your  Password")
        return PASSWORD  # Proceed to the next state (EMAIL)
    else:
        await update.message.reply_text("Please use the button to share your phone number.")
        return PHONE  # Stay in the current state (PHONE) until a contact is received

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration canceled.")
    return ConversationHandler.END


async def handle_confirm_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    username = user_data.get("username","botuser")
    phone = user_data.get('phone',"botphone")
    password = user_data.get('password')
    confirm_password = user_data.get('password_confirm')

    if password != confirm_password:
        await update.message.reply_text("Passwords do not match. Please start over.")
        return PASSWORD
    

    response = requests.post(f"{BACK_URL}/accounts/register/", data=user_data)

    print("response = ",response)

    if response.status_code == 201:  # Assume 201 means success
        await update.message.reply_text("Registration completed successfully!")
    else:
        print("response.json()=   ",response.json())
        await update.message.reply_text(f"Registration failed: {response.json().get('error', 'Unknown error')}")

    # del user_data[user_id]  # Clear user data after registration