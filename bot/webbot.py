import json
import requests
import logging
import random
import string
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
from register import *


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

BACK_URL = config('BACK_URL')


apiKey="DEFAULT_af37ed09-7a87-4d0a-92d4-822ac4eb3642"
				
headers = {
   "Auth":apiKey
}


def generate_nonce(length=64):
    characters = string.ascii_letters + string.digits + string.punctuation
    nonce = ''.join(random.choice(characters) for _ in range(length))
    return nonce



# Define conversation states
DEPOSIT_AMOUNT = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🎮 Play", callback_data='play'),
         InlineKeyboardButton("📝 Register",callback_data = "/register")],
        [InlineKeyboardButton("💰 Check Balance", callback_data='check_balance'),
         InlineKeyboardButton("💳 Deposit", callback_data='deposit')],
        [InlineKeyboardButton("📞 Contact Support", callback_data='contact_support'),
         InlineKeyboardButton("📚 Instruction", callback_data='instructions')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to Selam Bingo! Select an option:', reply_markup=reply_markup)


# Function to create the play options keyboard
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



def deposit_opitions_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
                [
                InlineKeyboardButton("Adiss pay", callback_data='adiss'),
                 InlineKeyboardButton("Manual", callback_data='manual')
                 ],
                 [
                InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')
 
                 ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup



async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = deposit_opitions_keyboard()  # Create the inline keyboard
    await update.message.reply_text("Select deposit method\nNote: Don't pay more than 2% as a transaction fee for each manual deposit", reply_markup=reply_markup)



async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = play_options_keyboard()  # Create the inline keyboard
    await update.message.reply_text("Choose a play option:", reply_markup=reply_markup)



# Function to create the play options keyboard
def instructions_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📝 Registraion", callback_data='register_instructions'),
            InlineKeyboardButton("🎮 Game play ", callback_data='play_instruction')
         ],
        [
            InlineKeyboardButton("💰 Deposit", callback_data='deposit_instruction'),
            InlineKeyboardButton("💰 Withdraw", callback_data='withdraw_instruction')
         ],
         [InlineKeyboardButton("🔙 Back to Menu", callback_data='back')]
    ]
    

    return InlineKeyboardMarkup(keyboard)





# Function to create the play options keyboard
def support_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📞 Support",  url='https://t.me/Selam_bingo_bot')],
    ]
    return InlineKeyboardMarkup(keyboard)



async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = support_options_keyboard()
    await update.message.reply_text("Contact us using support button.:", reply_markup=reply_markup)



async def instruction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = instructions_options_keyboard()  # Create the inline keyboard
    await update.message.reply_text("Choose a instruction option:", reply_markup=reply_markup)




async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    try:

        if query.data == 'play':
            await query.edit_message_text(
                text="Choose a play option:",
                reply_markup=play_options_keyboard()
            )

        elif query.data == 'instructions':
            await query.edit_message_text(
                text="Choose a play option:",
                reply_markup=instructions_options_keyboard()
            )

        elif query.data == 'contact_support':
            await query.edit_message_text(
                text="Choose a contact support:",
                reply_markup=support_options_keyboard()
            )

            


        elif query.data == 'register_instructions':
            chat_id = update.effective_chat.id
            local_video_path = './assets/register.mp4'
            caption = 'Regisrations instruction!'

            with open(local_video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file, caption=caption)


        elif query.data == 'check_balance':
            await query.edit_message_text(text="Your balance is 0 ETB.")

        elif query.data in ['10','20', '50','100']:

            player_id = query.from_user.id
            username = query.from_user.username
            bet_amount = query.data
            wallet_amount = 120 
            print("data = ",query.data)

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
                [InlineKeyboardButton("Adiss pay", callback_data='adiss'),
                 InlineKeyboardButton("Manual", callback_data='manual')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Select deposit method\nNote: Don't pay more than 2% as a transaction fee for each manual deposit", reply_markup=reply_markup)
        elif query.data == 'adiss':
            await query.edit_message_text(text="Please enter the amount you want to deposit:")
            return DEPOSIT_AMOUNT  # Proceed to the next state
        
        elif query.data == "register":
            await query.edit_message_text('Welcome! Use /register to start the registration process.')
        elif query.data == 'menu':
            await start(update, context) 
 
        else:
            await start(update, context) 
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
        amount = float(amount)
 
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
        response = requests.post(addispay_checkout_api_url, json=payload, headers=headers)
        checkout_url = None
        if response.status_code ==200:
            response_content = response.json()
            checkout_url= response_content["checkout_url"] + "/"+response_content["uuid"]

        if checkout_url:
            keyboard = [
                [InlineKeyboardButton("Open Adiss pay!", web_app=WebAppInfo(url=checkout_url))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("pay with Adiss pay", reply_markup=reply_markup)


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
        "instructions", 
        "instructions to play game"
        ),

      BotCommand(
        "support", 
        "Contact us"
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
    application = ApplicationBuilder().token("6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww").post_init(post_init).build()

    register_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('register', begin_register)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, handle_phone)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)],
            CONFIRM_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirm_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    deposit_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            DEPOSIT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('play', play_command))
    application.add_handler(CommandHandler("deposit",deposit_command))
    application.add_handler(CommandHandler('instructions', instruction_command))
    application.add_handler(CommandHandler('support', support_command))
    application.add_handler(deposit_conversation_handler)
    application.add_handler(register_conversation_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()