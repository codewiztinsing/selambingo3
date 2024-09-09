import json
import logging
import telegram
import requests
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler
from .register import conv_handler
import json

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)






from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext


# Define a function that will be called when the /start command is issued
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Check Balance", callback_data='check_balance'),
         InlineKeyboardButton("Deposit", callback_data='deposit')],
        [InlineKeyboardButton("Contact Support", callback_data='contact_support'),
         InlineKeyboardButton("Instruction", callback_data='instruction')],
        [InlineKeyboardButton("Play10", callback_data='play10'),
         InlineKeyboardButton("Play20", callback_data='play20')],
        [InlineKeyboardButton("Play50", callback_data='play50'),
         InlineKeyboardButton("Play100", callback_data='play100')],
        [InlineKeyboardButton("Play Demo", callback_data='play_demo')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text('Welcome to Selam Bingo! Select an option:', reply_markup=reply_markup)

# Define a callback function for button presses
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print("query answer = ",query)
    
    # Handle different button presses
    if query.data == 'check_balance':
        query.edit_message_text(text="Your balance is $100.")
    elif query.data == 'deposit':
        query.edit_message_text(text="Please follow the deposit instructions.")
    elif query.data == 'contact_support':
        query.edit_message_text(text="Contact support at support@example.com.")
    elif query.data == 'instruction':
        query.edit_message_text(text="Here are the instructions for playing.")
    elif query.data in ['play10', 'play20', 'play50', 'play100', 'play_demo']:
        data = query.data
       
        query.edit_message_text(text=f"You selected {query.data}.")






def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww")
        .build()
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()