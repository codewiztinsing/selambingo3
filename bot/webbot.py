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


# option command
async def start(update, context):
    keyboard = [
        [telegram.InlineKeyboardButton("Play 10", callback_data="Play10")],
        [telegram.InlineKeyboardButton("Play 20", callback_data="Play20")],
        [telegram.InlineKeyboardButton("Play 40", callback_data="Play40")],
        [telegram.InlineKeyboardButton("Play 50", callback_data='"Play50')],
        [telegram.InlineKeyboardButton("Play 60", callback_data="Play60")],
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)


async def button_handler(update, context):
    query = update.callback_query
    answer = await query.answer()

    print("query data=", query.data)
    print("answer=", answer)
    # Handle button clicks based on callback_data
    if query.data == "play10":
        # Do something for Play 10
        await update.effective_message.reply_text("You chose Play 10")
    elif query.data == "play20":
        # Do something for Play 20
        await update.effective_message.reply_text("You chose Play 20")


# Define a `/play` command handler.
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Please press the button below to choose a color via the WebApp.",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="start",
                web_app=WebAppInfo(url="https://addisbingo.com/userLogin?next=/"),
            )
        ),
    )


# Define a `/deposit` command handler.
async def cash_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text("cash with draw will be handled here")


# Define a `/deposit` command handler.
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Please Register",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="start",
                web_app=WebAppInfo(url="https://addisbingo.com/userLogin?next=/"),
            )
        ),
    )




async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text("payment will be handled here")

async def check_account_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    username = update.message.from_user.username
    print("user data = ",username)
    balance_data = requests.get(f"http://127.0.0.1:8000/balance?username= {username}")
    body  = json.loads(balance_data.text)
    print("balance = ",body['balance'])
    await update.message.reply_text(f"amount in your wallet = {body['balance']}")



# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=(
            f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
            f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )




from telegram import ReplyKeyboardMarkup, KeyboardButton

async def start(update, context):
    buttons = [
        [KeyboardButton("/register"),
        KeyboardButton("/balance"),
        KeyboardButton("/withdraw"),
        KeyboardButton("/load"),

        ],
        [KeyboardButton("/view")]
        ]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                            text="Please select an option:",
                            reply_markup=reply_markup)



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww")
        .build()
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("balance", check_account_balance))
    application.add_handler(CommandHandler("deposit", deposit))
    application.add_handler(CommandHandler("withdraw", cash_withdraw))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data)
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()