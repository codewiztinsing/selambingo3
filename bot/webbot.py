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
from datetime import datetime, timedelta

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

apiKey=  config('ARIF_SECRET')

				
headers = {
   "Auth":apiKey
}


def generate_nonce(length=64):
    characters = string.ascii_letters + string.digits + string.punctuation
    nonce = ''.join(random.choice(characters) for _ in range(length))
    return nonce



# Define conversation states
DEPOSIT_AMOUNT = range(1)
SCREENSHOT = range(2)
PHONE_NUMBER,WITHDRAW_AMOUNT_CONFIRM,WITHDRAW_AMOUNT_CANCEL,CHOOSE_PAYMENT_METHOD = range(2,6)


async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo[-1]
    file_id = photo.file_id
    file = await context.bot.get_file(file_id)
    file_path = file.file_path
    print("file_path = ",file_path)
    await update.message.reply_text("Thank you for choosing our services. To complete your payment, please via  {amount} ETB  to  via Telebirr to +251991221912. 📲 Once the payment has been processed, kindly send us a screenshot of the transaction confirmation for verification. 📸")
    return ConversationHandler.END

    
    


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



async def get_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    phone_number = update.message.text
    # Validate phone number format
    if not phone_number.startswith('09') or len(phone_number) != 10 or not phone_number.isdigit():
        await update.message.reply_text("Invalid phone number format. Please enter a valid phone number starting with 09 and 10 digits long.")
        return

    context.user_data['phone_number'] = phone_number

    await update.message.reply_text("Please enter the amount you want to withdraw:")
    return WITHDRAW_AMOUNT_CONFIRM

def deposit_opitions_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
                [
                InlineKeyboardButton("Arif pay", callback_data='arif'),
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
                    InlineKeyboardButton("Telebirr", callback_data='telebirr'),
                    InlineKeyboardButton("CBEbirr", callback_data='cbebirr')
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


async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = withdraw_opitions_keyboard()  # Create the inline keyboard
    await update.message.reply_text("Choose a withdraw method", reply_markup=reply_markup)


async def get_withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text
    phone_number = context.user_data.get('phone_number')
    # Check user's wallet balance before processing withdrawal
    telegram_user = update.effective_user.username
    user_id = update.effective_user.id
    wallet_response = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/')
    
    if wallet_response.status_code != 200:
        await update.message.reply_text("Error: Unable to check wallet balance. Please try again.")
        return ConversationHandler.END
        
    wallet_data = wallet_response.json()
    balance = wallet_data.get('balance', 0)
    
    if float(amount) > balance:
        await update.message.reply_text(f"Insufficient funds. Your current balance is {balance} ETB")
        return ConversationHandler.END


    session_url = "https://gateway.arifpay.net/api/checkout/session"
    headers = {
        "x-arifpay-key":"aXOIyscT4H6TO0yrR1V32ehuzXquwlux"
    }
    session_payload = {
            "cancelUrl": "https://api.selambingo.com/payments/cancelUrl/",
            "phone": phone_number,
            "email": "selambingo@gmail.com",
            "nonce": generate_nonce(),
            "errorUrl": "https://api.selambingo.com/payments/errorUrl/",
            "notifyUrl": "https://api.selambingo.com/payments/notifyUrl-withdraw/",
            "successUrl": "https://api.selambingo.com/payments/successUrl/",
            "paymentMethods": [
                "TELEBIRR_USSD" 
            ],
            "expireDate":  f"2025-09-05T03:45:27",
            "items": [
                {
                    "name": "with from selambingo",
                    "quantity": 1,
                    "price": float(amount),
                    "description": "with from selambingo"
                }
            ],
            "beneficiaries": [
                {
                    "accountNumber": "01320811436100", 
                    "bank": "AWINETAA", 
                    "amount": float(amount)
                }
            ],
            "lang": "EN"
        }

    response = requests.post(session_url, headers=headers, json=session_payload)
    session_data = response.json()
    session_id = session_data.get('data').get('sessionId')
    withdraw_url = f"https://telebirr-b2c.arifpay.net/api/Telebirr/b2c/transfer"
    withdraw_payload = {
        "sessionId": session_id,
        "phoneNumber": phone_number
    }
    withdraw_response = requests.post(withdraw_url, headers=headers, json=withdraw_payload,verify=False)
    withdraw_data = withdraw_response.json()
    if withdraw_response.status_code == 200:
        withdraw_payload = {
            "userId": user_id,
            "amount": amount
        }
        withdraw_response = requests.post("https://api.selambingo.com/payments/withdraw/", json=withdraw_payload)
        if withdraw_response.status_code == 200:
            await update.message.reply_text("✅ Withdrawal request sent successfully! 🎉\n\n📱 Please check your Telebirr app for the transfer.\n\n💰 Your funds will be available shortly.\n\n🙏 Thank you for using Selam Bingo!")
        else:
            await update.message.reply_text("Failed to send withdrawal request. Please try again.")
        
    else:
        await update.message.reply_text("Failed to send withdrawal request. Please try again.")
    
    
    return ConversationHandler.END



async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = play_options_keyboard() 
    user_id = update.effective_user.id
    username = update.effective_user.username
    try:
        balance = requests.get(f'{BACK_URL}/payments/balance?username={username}').json().get('results',[]).get("results",[])
        balance = balance['results'][0]['totalTransactionAmount']
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
    username = query.from_user.username
    await query.answer()
  

    try:
        if query.data in ['10', '20', '50', '100']:
            user_id = query.from_user.id
            
            # Check if user is registered
            response = requests.get(f'{BACK_URL}/accounts/filter-users/{user_id}/')
            print("response = ",response)
            if response.status_code != 200:
                await query.edit_message_text(
                    text="You need to register first before playing. Use the /register command.",
                    reply_markup=instructions_options_keyboard()
                )
                return

            # Check user's balance
            balance = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/').json().get('balance',0)
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
            wallet_amount = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/').json().get('balance',0)
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

        elif query.data == 'withdraw_confirm':
            return WITHDRAW_AMOUNT_CONFIRM

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
            user_id = query.from_user.id
            # Get wallet balance from API
            response = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/')
            balance = response.json().get('balance', 0)
           

            # Create payment summary with user details
            payment_summary = (
                f"👤 Username: @{username}\n"
                "------------------------\n"
                f"👤 First Name: {first_name}\n"
                 "------------------------\n"
                f"👤 Last Name: {last_name}\n"
                "------------------------\n"
                f"💰 Wallet Balance: {balance:.2f} ETB\n"
                "------------------------\n"
                "💳 Payment Methods Available:\n"
                "• Arif Pay\n" 
                "• Manual Transfer\n\n"
                "Use /deposit to add funds"
            )
            await query.edit_message_text(text=payment_summary)
            return
            
            await query.edit_message_text(text=f"Your balance is {balance} ETB.")

        elif query.data in ['10','20', '50','100']:

            player_id = query.from_user.id
            user_id = query.from_user.id
            username = query.from_user.username or query.from_user.first_name
            bet_amount = query.data
        
            wallet_amount = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/').json().get('balance',0)
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
                [InlineKeyboardButton("Arif pay", callback_data='arif'),
                 InlineKeyboardButton("Manual", callback_data='manual')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Select deposit method\nNote: Don't pay more than 2% as a transaction fee for each manual deposit", reply_markup=reply_markup)
        elif query.data == 'arif':
            await query.edit_message_text(text="Please enter the amount you want to deposit:")
            return DEPOSIT_AMOUNT  # Proceed to the next state
        
        elif query.data == 'telebirr':
            await query.edit_message_text("እባኮትን ስልክ ቁጥርዎን በቅርጸት ያስገቡ፡ 09xxxxxxxx")
            return PHONE_NUMBER  # Proceed to get phone number state


        elif query.data == 'manual':
            await query.edit_message_text(text="Please enter the amount you want to deposit:")
            amount = query.message.text
        
        
            content = f"""
                Thank you for choosing our services. To complete your payment, please via  {amount} ETB  to  via Telebirr to +251991221912. 📲 Once the payment has been processed, kindly send us a screenshot of the transaction confirmation for verification. 📸
                If you have any questions or require any assistance, please do not hesitate to contact us. We appreciate your business and look forward to serving you. 🙏
                Best regards
                """
    
            await query.edit_message_text(text=content)
            return SCREENSHOT  # Proceed to the next state to get the screenshot
       

        elif query.data == 'cancel':
            await query.edit_message_text(text="Withdrawal request cancelled.")
            return ConversationHandler.END


        
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
    try:
        amount = float(update.message.text)
        user_id = update.message.from_user.id
        first_name = update.message.from_user.first_name or "Bot user"
        last_name = update.message.from_user.last_name or "Bot Father"
        username = update.message.from_user.username

        # Check if user exists in database
        user_response = requests.get(f"{BACK_URL}/accounts/filter-users/{user_id}/")
        if user_response.status_code != 200:
            keyboard = [
                [InlineKeyboardButton("Register", callback_data='register')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "You need to register first before making a deposit. Please click Register below.",
                reply_markup=reply_markup
            )
            return ConversationHandler.END

        user_data = user_response.json()
        phone = user_data.get('phone')
        
        if not phone:
            await update.message.reply_text(
                "Your phone number is not registered. Please register first using /register command."
            )
            return ConversationHandler.END

        logger.info(f"Received deposit amount: {amount}")
        reference_no = f"selam_bingo_{first_name}_{datetime.now().second}"

        arifpay_checkout_api_url = "https://gateway.arifpay.net/api/checkout/telebirr-ussd/transfer/direct"
        # Convert datetime to ISO format string
        expiry_time = (datetime.now() + timedelta(minutes=5)).isoformat()
        
        payload = {
            "cancelUrl": "https://api.selambingo.com/payments/cancelUrl/",
            "phone": phone,
            "email": "selambingo@gmail.com",
            "nonce": generate_nonce(),
            "errorUrl": "https://api.selambingo.com/payments/errorUrl/",
            "notifyUrl": "https://api.selambingo.com/payments/notifyUrl/",
            "successUrl": "https://api.selambingo.com/payments/successUrl/",
            "paymentMethods": [
                "TELEBIRR_USSD"
            ],
            "expireDate": expiry_time,  # Now using the string format
            "items": [
                {
                    "name": "bingo game deposit",
                    "quantity": 1,
                    "price": amount,
                    "description": "Arif pay for selam bingo",
                }
            ],
            "beneficiaries": [
                {
                    "accountNumber": "01320811436100", 
                    "bank": "AWINETAA",
                    "amount": amount
                }
            ],
            "lang": "EN"
        }
        
        headers = {
            "x-arifpay-key": "aXOIyscT4H6TO0yrR1V32ehuzXquwlux"
        }

        response = requests.post(arifpay_checkout_api_url, json=payload, headers=headers)
        if response.status_code == 200:
            session_id = response.json().get("data", {}).get("sessionId")
            user_id = update.message.from_user.id

            session_payload = {
                "user_id": user_id,
                "session_id": session_id,
                "reference_no": reference_no,
                "amount": amount,
                "payment_id": "arifpay",
                "status": "PENDING"
            }
            session_response = requests.post(f"{BACK_URL}/payments/session/", json=session_payload)
            if session_response.status_code == 201:
                await update.message.reply_text(
                    f"💰 Please complete your payment when Telebirr popup reaches you 📱✨"
                
                )

            else:
                await update.message.reply_text("Failed to create payment session. Please try again later.")
           

        else:
            await update.message.reply_text("Failed to initiate payment. Please try again later.")
  
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
    except Exception as e:
        logger.error(f"Error processing deposit: {str(e)}")
        await update.message.reply_text("An error occurred. Please try again later.")
    
    return ConversationHandler.END



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


async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = requests.get(f'{BACK_URL}/accounts/all-users/').json()  # Fetch all users
   
    text = " ውድ ሰላም ቢንጎ ተጫዋቾች .በአሁኑ ጊዜ በጥገና ላይ ነን እና በቅርቡ እንመለሳለን! ለትዕግስትዎ እናመሰግናለን። 🛠️"
    for user in users:

        sent_users = set()  # Keep track of users to whom messages have been sent
        if user['telegram_id'] not in sent_users:
            sent_users.add(user['telegram_id'])  # Mark user as sent
            try:
                await context.bot.send_message(chat_id=user['telegram_id'], text=text)
            except Exception as e:
                continue
        else:
            continue  # Skip sending message if already sent
      
  


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    register_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('register', begin_register)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, handle_phone)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    deposit_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            DEPOSIT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount)],
            PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_number)],
            WITHDRAW_AMOUNT_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_withdraw_amount)]
           
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
    application.add_handler(CommandHandler('broadcast', broadcast_message))

  
    # application.add_handler(withdraw_conversation_handler)
    application.add_handler(register_conversation_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()