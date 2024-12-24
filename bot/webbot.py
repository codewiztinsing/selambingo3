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
BOT_TOKEN = config('BOT_TOKEN')
TEST_ADISS_SECRET = config('TEST_ADISS_SECRET')

apiKey=  config('ADISS_SECRET')
test_apiKey = config('TEST_ADISS_SECRET')

				
headers = {
   "Auth":apiKey
}


def generate_nonce(length=64):
    characters = string.ascii_letters + string.digits + string.punctuation
    nonce = ''.join(random.choice(characters) for _ in range(length))
    return nonce



# Define conversation states
DEPOSIT_AMOUNT = range(1)
WITHDRAW_AMOUNT = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🎮 Play", callback_data='play'),
         InlineKeyboardButton("📝 Register",callback_data = "register")],
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


def withdraw_opitions_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
                [
                InlineKeyboardButton("Adiss pay", callback_data='withdraw_virtual'),
                 InlineKeyboardButton("Manual", callback_data='withdraw_manual')
                 ],
                 [
                InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')
 
                 ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    username = update.message.from_user.username
    print("username = ",username)
    try:
        response = requests.post(f'{BACK_URL}/payments/withdraw/', json={
            'username': username,
            'amount': 100
        })
        if response.status_code == 200:
            update.message.reply_text("Withdrawal request submitted successfully!")
        else:
            update.message.reply_text("Error processing withdrawal. Please try again later.")
    except Exception as e:
        logger.error(f"Error processing withdrawal: {e}")
        update.message.reply_text("An error occurred. Please try again later.")
   
    return ConversationHandler.END

async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = deposit_opitions_keyboard()  # Create the inline keyboard
    await update.message.reply_text("Select deposit method\nNote: Don't pay more than 2% as a transaction fee for each manual deposit", reply_markup=reply_markup)


async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = withdraw_opitions_keyboard()  # Create the inline keyboard
    await update.message.reply_text("Choose a withdraw method", reply_markup=reply_markup)



async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = play_options_keyboard() 
    user_id = update.effective_user.id
    username = update.effective_user.username
    try:
        balance = requests.get(f'{BACK_URL}/payments/balance?username={username}').json().get('results',[]).get("results",[])
        balance = balance['results'][0]['totalTransactionAmount']
        print("balance = ",balance)
        print("balance = ",balance)
    except Exception as e:
        print(f"Error getting wallet balance: {e}")
  
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
        if query.data in ['10', '20', '50', '100']:
            username = query.from_user.username
            
            # Check if user is registered
            registration_response = requests.get(f'{BACK_URL}/accounts/filter-users/?username={username}')
            if registration_response.status_code != 200:
                await query.edit_message_text(
                    text="You need to register first before playing. Use the /register command.",
                    reply_markup=instructions_options_keyboard()
                )
                return

            # Check user's balance
            # balance = requests.get(f'{BACK_URL}/payments/balance?username={username}').json().get("balance",{}).get("results",{})[0].get("totalTransactionAmount",0)
            balance = requests.get(f'{BACK_URL}/payments/wallet/{username}/').json().get('balance',0)
            bet_amount = int(query.data)
          
            
            if balance < bet_amount:
                await query.edit_message_text(
                    text=f"Insufficient balance. Your current balance is {balance} ETB. Please deposit more to play.",
                    reply_markup=deposit_opitions_keyboard()
                )
                return

            player_id = query.from_user.id
            web_app_url = (
                f"https://selambingo.com/?playerId={player_id}&name={username}&betAmount={bet_amount}&wallet_amount={balance}"
            )
        if query.data == 'play_demo':
            player_id = query.from_user.id
            username = query.from_user.username
            bet_amount = 0  # Demo game has no bet amount
            wallet_amount = requests.get(f'{BACK_URL}/payments/wallet/{username}/').json().get('balance',0)
            web_app_url = (
                f"https://selambingo.com/?playerId={player_id}&name={username}&betAmount={bet_amount}&wallet_amount={wallet_amount}&demo=true"
            )
            await query.edit_message_text(
                text=f"Starting demo game...",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Play Demo", web_app=WebAppInfo(url=web_app_url))
                ]])
            )

            return ConversationHandler.END


        if query.data == 'play' :
            await query.edit_message_text(
                text="Choose a play option:",
                reply_markup=play_options_keyboard()
            )

        elif query.data == 'instructions':
            web_app_url = "https://api.selambingo.com/insturction/"
            await query.edit_message_text(
                text="Game Instructions",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("View Instructions", web_app=WebAppInfo(url=web_app_url))
                ]])
            )

            # await query.edit_message_text(
            #     text="Choose a play option:",
            #     reply_markup=instructions_options_keyboard()
            # )

        elif query.data == 'contact_support':
            await query.edit_message_text(
                text="Choose a contact support:",
                reply_markup=support_options_keyboard()
            )

            


        elif query.data == 'register_instructions':
            chat_id = update.effective_chat.id
            local_video_path = './assets/register.mp4'
            caption = 's instruction!'

            with open(local_video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file, caption=caption)

        elif query.data == 'deposit_instruction':
            chat_id = update.effective_chat.id
            local_video_path = './assets/deposit.mp4'
            caption = 'deposit instruction!'

            with open(local_video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file, caption=caption)

        elif query.data == 'play_instruction':
            chat_id = update.effective_chat.id
            local_video_path = './assets/play.mp4'
            caption = 'play instruction!'

            with open(local_video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file, caption=caption)


        elif query.data == 'check_balance':
            
            username = query.from_user.username
            first_name = query.from_user.first_name
            last_name = query.from_user.last_name
            # Get wallet balance from API
            response = requests.get(f'{BACK_URL}/payments/wallet/{username}/')
            balance = response.json().get('balance', 0)
           

            # Create payment summary with user details
            payment_summary = (
                f"👤 Username: @{username}\n"
                "------------------------\n"
                f"👤 First Name: {first_name}\n"
                 "------------------------\n"
                f"� Last Name: {last_name}\n"
               
                "------------------------\n"
                f"�💰 Wallet Balance: {balance:.2f} ETB\n"
                "------------------------\n"
                "💳 Payment Methods Available:\n"
                "• Adiss Pay\n" 
                "• Manual Transfer\n\n"
                "Use /deposit to add funds"
            )
            await query.edit_message_text(text=payment_summary)
            return
            
            await query.edit_message_text(text=f"Your balance is {balance} ETB.")

        elif query.data in ['10','20', '50','100']:

            player_id = query.from_user.id
            username = query.from_user.username or query.from_user.first_name
            bet_amount = query.data
        
            wallet_amount = requests.get(f'{BACK_URL}/payments/wallet/{username}/').json().get('balance',0)
            print("data = ",query.data)

            web_app_url = (
                f"https://selambingo.com/?playerId={player_id}&name={username}&betAmount={bet_amount}&wallet_amount={wallet_amount}"
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
        
        elif query.data == 'withdraw_virtual':
            print("before entering withdraw_amount")
            return WITHDRAW_AMOUNT  # Need to define WITHDRAW_AMOUNT = range(1) at the top with other states
        
         
        
        
        elif query.data == "register":
           
            # return begin_register(update,context)
            await query.edit_message_text('Welcome! Use /register to start the registration process.')
          
        elif query.data == 'menu':
            keyboard = [
                [InlineKeyboardButton("Play Game", callback_data='play'),
                 InlineKeyboardButton("Check Balance", callback_data='check_balance')],
                [InlineKeyboardButton("Deposit", callback_data='deposit'),
                 InlineKeyboardButton("Register", callback_data='register')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Welcome to Selam Bingo! Please select an option:", reply_markup=reply_markup)
            
            
 
        else:

            keyboard = [
                [InlineKeyboardButton("Play Game", callback_data='play'),
                 InlineKeyboardButton("Check Balance", callback_data='check_balance')],
                [InlineKeyboardButton("Deposit", callback_data='deposit'),
                 InlineKeyboardButton("Register", callback_data='register')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Welcome to Selam Bingo! Please select an option:", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error handling query: {query.data} - {e}")
        await query.edit_message_text(text="An error occurred. Please try again.")

async def deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    amount =  float(update.message.text)
    query = update.callback_query
    first_name =  update.message.from_user.first_name or "Bot user"
    last_name =  update.message.from_user.last_name or "Bot Father"
    username = update.message.from_user.username
    phone = None
    if update.message.from_user:
        phone = requests.get(f"{BACK_URL}/accounts/filter-users/?username={update.message.from_user.username}").json()
        phone = phone.get('phone',None)
        if phone is None:
            keyboard = [
                [InlineKeyboardButton("Register", callback_data='register')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "You need to register first before making a deposit. Please click Register below.",
                reply_markup=reply_markup
            )
            return ConversationHandler.END
        
        

    logger.info(f"Received deposit amount: {amount}")

    try:
        amount = float(amount)
 
        reference_no = f"selam_bingo_{first_name}_{datetime.now().second}"
        logger.info(f"Received deposit amount: {amount}")

        data = {
        "redirect_url": "https://t.me/SelamBingo_bot",
        "cancel_url": "https://api.selambingo.com/cancel",
        "success_url": "https://api.selambingo.com/payments/success/",
        "error_url": "https://api.selambingo.com/payments/error/",
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
            "username": username,
            "telecomOperator": "ethio_telecom"
            
        },
        "phone_number": phone,
        "session_expired": "5000",
        "total_amount": f"{amount}",
        "tx_ref": "selam_pay_" + generate_nonce(64),
        }
    
        addispay_checkout_api_url="https://api.addispay.et/checkout-api/v1/create-order"
        payload = {
        "data":data,
        "message":"test message"
        }
        response = requests.post(addispay_checkout_api_url, json=payload, headers=headers)
    
        print("response = ",response)
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
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

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
    wihtdraw_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            WITHDRAW_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('play', play_command))
    application.add_handler(CommandHandler("deposit",deposit_command))
    application.add_handler(CommandHandler('instructions', instruction_command))
    application.add_handler(CommandHandler('support', support_command))
    application.add_handler(CommandHandler('withdraw', withdraw_command))
    application.add_handler(deposit_conversation_handler)
    application.add_handler(wihtdraw_conversation_handler)
    application.add_handler(register_conversation_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()