from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes
# from telegram import filters  # Updated import for filters
import requests
import os
from decouple import config
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import requests


BACK_URL = config('BACK_URL')
user_data = {}  # Dictionary to hold user registration data temporarily

# Define states for conversation
PHONE,EMAIL,PASSWORD,CONFIRM_PASSWORD = range(4)



async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id]['email'] = update.message.text

    await update.message.reply_text("Please provide your password:")
    return PASSWORD

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id]['password'] = update.message.text

    await update.message.reply_text("Please confirm your password:")
    return CONFIRM_PASSWORD

async def handle_confirm_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id]['confirm_password'] = update.message.text

    username = user_data[user_id]['username']
    phone = user_data[user_id]['phone']
    email = user_data[user_id]['email']
    password = user_data[user_id]['password']
    confirm_password = user_data[user_id]['confirm_password']

    if password != confirm_password:
        await update.message.reply_text("Passwords do not match. Please start over.")
        return

    response = requests.post(f"{BACK_URL}/accounts/register/", json={
        "username": username,
        "phone": phone,
        "email": email,
        "password": password,
        "password_confirm": confirm_password
    })

    if response.status_code == 201:  # Assume 201 means success
        await update.message.reply_text("Registration completed successfully!")
    else:
        await update.message.reply_text(f"Registration failed: {response.json().get('error', 'Unknown error')}")

    del user_data[user_id]  # Clear user data after registration

async def begin_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username if update.message.from_user.username else "Not provided"
    
    await update.message.reply_text(f"Welcome! Your username is: {username}. Please share your phone number.")

    # Create a button to share phone number
    phone_button = KeyboardButton("Share Phone Number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[phone_button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Click the button below to share your phone number:", reply_markup=reply_markup)

    return PHONE  # Move to the PHONE state

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        phone_number = update.message.contact.phone_number
        await update.message.reply_text(f"Thank you ! Your phone number is: {phone_number}")
        return EMAIL
    else:
        await update.message.reply_text("Please use the button to share your phone number.")
        return EMAIL

    return EMAIL  # End the conversation

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration canceled.")
    return ConversationHandler.END
