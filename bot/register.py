import uuid
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackContext,
    filters
)
import logging
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from queue import Queue
import requests

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
# Define conversation states
CHOOSING, TYPING_CHOICE, TYPING_REPLY,PASSWORD_REPLY,CALL_API = range(5)


# Define handler functions for the conversation
async def start(update: Update, context) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    await update.message.reply_text(
        "1. register \n2. delete \n 3. update"
    )
    user_choice = update.message.text
    context.user_data["choice"] = user_choice
    return TYPING_REPLY


async def received_username(update: Update, context: CallbackContext) -> int:
    """Store the user reply and end the conversation."""
    await update.message.reply_text(
        f"What is your  phone number?"
    )
    phone = update.message.text
    context.user_data["phone"] = phone
    return PASSWORD_REPLY


async def received_password(update: Update, context: CallbackContext) -> int:
    """Store the password reply and end the conversation."""
    await update.message.reply_text(
        f"Please input username "
    )
    username = update.message.text
    context.user_data["username"] = username
    return CALL_API

async def call_api(update: Update, context: CallbackContext) -> int:
    phone = context.user_data['phone']
    password = str(uuid.uuid4())
    user = update.message.from_user

    data     = requests.post("http://127.0.0.1:8000/auth/users/",json = {
        'username':user.username,
        'password':f"{password}",
        'phone':phone
    })
    if data.status_code != 400:
        await update.message.reply_text(f"Registred Sucessfully!")
    else:
        await update.message.reply_text(f"Already registered!")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the conversation and end the ConversationHandler."""
    user = update.message.from_user
    await update.message.reply_text("Okay, let me know if you need anything else!")
    return ConversationHandler.END



conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", start)],
    states={
        # CHOOSING: [MessageHandler(filters.Regex(r'^[0-9]$'), make_choice)],
        TYPING_REPLY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_username)
        ],

        PASSWORD_REPLY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_password)
        ],


        CALL_API : [
            MessageHandler(filters.TEXT & ~filters.COMMAND, call_api)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
