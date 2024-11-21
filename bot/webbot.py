import json
import logging
import random
from chapa import AsyncChapa
from decouple import config
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler,
)
from datetime import datetime
from telegram import BotCommand
from .payments import make_request,generate_nonce

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

BACK_URL = config('BACK_URL')

# Define conversation states
DEPOSIT_AMOUNT = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Register", callback_data='register')], 
        [InlineKeyboardButton("Check Balance", callback_data='check_balance'),
         InlineKeyboardButton("Deposit", callback_data='deposit')],
        [InlineKeyboardButton("Contact Support", callback_data='contact_support'),
         InlineKeyboardButton("Instruction", callback_data='instruction')],
        [InlineKeyboardButton("Play10", callback_data='10'),
         InlineKeyboardButton("Play20", callback_data='20')],
        [InlineKeyboardButton("Play50", callback_data='50'),
         InlineKeyboardButton("Play100", callback_data='100')],
        [InlineKeyboardButton("Play Demo", callback_data='play_demo')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to Selam Bingo! Select an option:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'check_balance':
            await query.edit_message_text(text="Your balance is $100.")


        if query.data == "register":
           
            keyboard = [
                [InlineKeyboardButton("Share your Phone", callback_data='begin_register')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Telegram profile will be used to register you in bot", reply_markup=reply_markup)

        elif query.data in ['10','20' '50','100']:

            player_id = query.from_user.id
            username = query.from_user.username
            bet_amount = query.data
            wallet_amount = 120  # Assuming this is a fixed value for demonstration

            web_app_url = (
                f"https://selambingo.onrender.com/?playerId={player_id}&name={username}&betAmount={bet_amount}&wallet_amount={wallet_amount}"
            )

            keyboard = [
                [InlineKeyboardButton("Open Selam Bingo!", web_app=WebAppInfo(url=web_app_url))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text("Start playing selam bingo", reply_markup=reply_markup)

        elif query.data == 'deposit':
            keyboard = [
                [InlineKeyboardButton("Chapa", callback_data='chapa'),
                 InlineKeyboardButton("Manual", callback_data='manual')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Select deposit method\nNote: Don't pay more than 2% as a transaction fee for each manual deposit", reply_markup=reply_markup)
        elif query.data == 'chapa':
            await query.edit_message_text(text="Please enter the amount you want to deposit:")
            return DEPOSIT_AMOUNT  # Proceed to the next state

        elif query.data == 'begin_register':
            user_profile = query.from_user
            print("user profile = ",user_profile)
            await query.message.reply_text("Register completed")

           
        else:
            await query.edit_message_text(text="Unknown option selected.")
    except Exception as e:
        logger.error(f"Error handling query: {query.data} - {e}")
        await query.edit_message_text(text="An error occurred. Please try again.")

async def deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    amount =  float(update.message.text)
    query = update.callback_query
    first_name =  update.message.from_user.first_name or "Bot user"
    last_name =  update.message.from_user.last_name or "Bot Father"
    username = update.message.from_user.username
    phone = "0991221912"
    logger.info(f"Received deposit amount: {amount}")

    try:
        amount = float(amount)  # Convert to float
        chapa = AsyncChapa('CHASECK_TEST-vlw3GDzGJjCYI2GU9FDfInYk1L2t4KAk')
 
        reference_no = f"selam_bingo_{first_name}_{datetime.now().second}"
        logger.info(f"Received deposit amount: {amount}")
        addispay_checkout_api_url="https://uat.api.addispay.et/checkout-api/v1/create-order"

        data = {
        "redirect_url": "https://selambingo.onrender.com/",
        "cancel_url": "https://selambingo.onrender.com/cancel",
        "success_url": "https://selambingo.onrender.com/",
        "error_url": "https://selambingo.onrender.com/",
        "order_reason": "payament for selam bingo bot",
        "currency": "ETB",
        "email": f"{first_name}@gmail.com",
        "first_name": first_name,
        "last_name": last_name,
        "nonce":  "selam_pay_" + generate_nonce(64),
        "order_detail": {
            "amount":float(amount),
            "description": "the transcationt to deposit amount in my bot wallet",
            "items": "single bot transcation",
            "phoneNumber": phone,
            "telecomOperator": "ethio_telecom",
            "image": "https://images.app.goo.gl/pYmev5W8J5AXpBin7"
        },
        "phone_number": phone,
        "session_expired": "5000",
        "total_amount": f"{amount}",
        "tx_ref": "selam_pay_" + generate_nonce(64),
        }
    
    
    
        addispay_checkout_api_url="https://uat.api.addispay.et/checkout-api/v1/create-order"

      
        payload = {
        "data":data,
        "message":"test message"
        }


        checkout_url =   make_request(payload,addispay_checkout_api_url)
        logger.info(f"checkout_url from backend: {checkout_url}")
  
        # print("checkoout url = ",checkout_url)
        if checkout_url:
            await update.message.reply_text(
                "Open web page",
                reply_markup=ReplyKeyboardMarkup.from_button(
                    KeyboardButton(
                        text="Open Chapa!",
                        web_app=WebAppInfo(url=checkout_url),
                    )
                ),
            )
     
     
        return ConversationHandler.END  # End the conversation
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
    except Exception as e:
        logger.error(f"Error processing deposit: {e}")
        await update.message.reply_text("An error occurred. Please try again.")




async def request_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    phone_button = KeyboardButton("Share my phone number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[phone_button]], one_time_keyboard=True)
    
    await update.message.reply_text(
        "Please share your phone number:",
        reply_markup=reply_markup
    )




async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    amount =  float(update.message.text)
    query = update.callback_query
    first_name =  update.message.from_user.first_name
    username = update.message.from_user.username

    logger.info(f"Received deposit amount: {amount}")
    addispay_checkout_api_url="https://uat.api.addispay.et/checkout-api/v1/create-order"
    checkout_url =   make_request(payload,addispay_checkout_api_url)
    
    logger.info(f"checkout_url checkout_url amount: {checkout_url}")

    try:
        addispay_checkout_api_url="https://uat.api.addispay.et/checkout-api/v1/create-order"

        checkout_url =   make_request(payload,addispay_checkout_api_url)
        logger.info(f"checkout_url from backend: {checkout_url}")
  
        # print("checkoout url = ",checkout_url)
        if checkout_url:
            await update.message.reply_text(
                "Open web page",
                reply_markup=ReplyKeyboardMarkup.from_button(
                    KeyboardButton(
                        text="Open Chapa!",
                        web_app=WebAppInfo(url=checkout_url),
                    )
                ),
            )
     
        return ConversationHandler.END  # End the conversation
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
    except Exception as e:
        logger.error(f"Error processing deposit: {e}")
        await update.message.reply_text("An error occurred. Please try again.")


all_public_commands_descriptions = [
    BotCommand(
        "start", 
        "start the bot"
    ),

    BotCommand(
        "play", 
        "start playing"
        ),
    BotCommand(
        "demo", 
        "start playing demo game"
        ),
    BotCommand(
        "register", 
        "register for an account"
        ),
 
    BotCommand(
        "deposit", 
        "Deposit funds into your account"
        ),

            BotCommand(
        "withdraw", 
        "withdraw funds"
        ),
    BotCommand(
        "transfer", 
        "transfer funds to another user"
        ),
 
    BotCommand(
        "convert", 
        "convert coins to wallet"
        ),

          BotCommand(
        "change_name", 
        "Change your account names"
        ),

            BotCommand(
        "game_history", 
        "Check your game history"
        ),
    BotCommand(
        "check_transcation", 
        "Check your transcation history"
        ),
 
    BotCommand(
        "invite", 
        "Invite your friends"
        )
    ]




async def post_init(app):
    await app.bot.set_my_commands(all_public_commands_descriptions)


def main() -> None:
    # application = (
    #     Application.builder()
    #     .token("6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww")
    #     .build()
    # )
    application = ApplicationBuilder().token("6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww").post_init(post_init).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            DEPOSIT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()