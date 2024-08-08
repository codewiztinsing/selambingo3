from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackContext,
    filters,
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

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
# Define conversation states
CHOOSING, TYPING_CHOICE, TYPING_REPLY = range(3)


# Define handler functions for the conversation
async def start(update: Update, context) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    await update.message.reply_text(
        "Hi! I'm a bot that helps you register for an event. Let's get started."
    )

    return CHOOSING


async def make_choice(update: Update, context: CallbackContext) -> int:
    """Store the selected option and ask for a reply."""
    user_choice = update.message.text
    context.user_data["choice"] = user_choice
    await update.message.reply_text(
        f"You chose {user_choice}. What is your question about this?"
    )
    return TYPING_REPLY


async def received_information(update: Update, context: CallbackContext) -> int:
    """Store the user reply and end the conversation."""
    text = update.message.text
    context.user_data["reply"] = text
    await update.message.reply_text("Thank you for your feedback!")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the conversation and end the ConversationHandler."""
    user = update.message.from_user
    await update.message.reply_text("Okay, let me know if you need anything else!")
    return ConversationHandler.END


# Set up the ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [
            MessageHandler(filters.Regex("^(Option 1|Option 2|Option 3)$"), make_choice)
        ],
        TYPING_REPLY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_information)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
