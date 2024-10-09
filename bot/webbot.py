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
                [InlineKeyboardButton("Chapa", callback_data='chapa'),
                 InlineKeyboardButton("Manual", callback_data='manual')
                 ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Select deposit method\nNote: Don't pay more than 2% as a transaction fee for each manual deposit", reply_markup=reply_markup)

        elif query.data in ['10','20' '50','100']:
            print("data=",query.data)
            print("username=",query.from_user.username)
            await query.message.reply_text(
                    "Open web page",
                    reply_markup=ReplyKeyboardMarkup.from_button(
                        KeyboardButton(
                            text="Open game!",
                            web_app=WebAppInfo(url=f"https://selambingo.onrender.com/?playerId=1&name={query.from_user.username}&betAmount={query.data}"),
                        )
                    ),
                )
        

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
        else:
            await query.edit_message_text(text="Unknown option selected.")
    except Exception as e:
        logger.error(f"Error handling query: {query.data} - {e}")
        await query.edit_message_text(text="An error occurred. Please try again.")

async def deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    amount =  float(update.message.text)
    query = update.callback_query
    first_name =  update.message.from_user.first_name
    username = update.message.from_user.username

    logger.info(f"Received deposit amount: {amount}")

    try:
        amount = float(amount)  # Convert to float
        chapa = AsyncChapa('CHASECK_TEST-vlw3GDzGJjCYI2GU9FDfInYk1L2t4KAk')
        print("date time = ",datetime.now())
        reference_no = f"selam_bingo_{first_name}_{datetime.now().second}"
        response = await chapa.initialize(
            email=f"{first_name}@gmail.com",

            amount=amount,
            currency="ETB",
            first_name=first_name,
            last_name=username,
            tx_ref=reference_no,
            callback_url="https://selambingo.onrender.com/"
        )
     
        checkout_url = response['data']['checkout_url']
        print("checkoout url = ",checkout_url)
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



async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    amount =  float(update.message.text)
    query = update.callback_query
    first_name =  update.message.from_user.first_name
    username = update.message.from_user.username

    logger.info(f"Received deposit amount: {amount}")

    try:
        amount = float(amount)  # Convert to float
        chapa = AsyncChapa('CHASECK_TEST-vlw3GDzGJjCYI2GU9FDfInYk1L2t4KAk')
        reference_no = f"selam_bingo_{first_name}_{datetime.now().second}"
        response = await chapa.initialize(
            email=f"{first_name}@gmail.com",

            amount=amount,
            currency="ETB",
            first_name=first_name,
            last_name=username,
            tx_ref=reference_no,
            callback_url="https://selambingo.onrender.com/"
        )
     
        checkout_url = response['data']['checkout_url']
        print("checkoout url = ",checkout_url)
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




def main() -> None:
    application = (
        Application.builder()
        .token("6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww")
        .build()
    )

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