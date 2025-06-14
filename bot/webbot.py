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

BACK_URL = "https://api.bilenbingo.com"
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
GET_DEPOSIT_AMOUNT,WITHDRAW_AMOUNT_CONFIRM,WITHDRAW_AMOUNT_CANCEL,CHOOSE_PAYMENT_METHOD,GET_WITHDRAW_ACCOUNT,GET_TRANSCATION_DETAILS = range(2,8)

CONVERSATION_TIMEOUT = 300  # 5 minutes




    
    


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
    await update.message.reply_text('Welcome to Bilen Bingo! Select an option:', reply_markup=reply_markup)
    context.job_queue.run_once(conversation_timeout, CONVERSATION_TIMEOUT, chat_id=update.effective_chat.id)
    return SOME_STATE


# Function to create the play options keyboard
def play_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🎮 Play 10", callback_data='10'),
         InlineKeyboardButton("🎮 Play 20", callback_data='20')],
        [InlineKeyboardButton("🎮 Play 50", callback_data='50'),
         InlineKeyboardButton("🎮 Play 100", callback_data='100')],
        [InlineKeyboardButton("🎮 Play Demo", callback_data='play_demo'),
         InlineKeyboardButton("🔙 Back to Menu", callback_data='back')
         ],
    ]
    return InlineKeyboardMarkup(keyboard)



async def get_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   
    await update.message.reply_text("Please enter the amount you want to withdraw:")
    return WITHDRAW_AMOUNT_CONFIRM

def deposit_opitions_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
              
                 [
                InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')
 
                 ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def withdraw_opitions_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📱 Telebirr", callback_data='withdraw_telebirr')],
        [InlineKeyboardButton("🏦 CBE Bank", callback_data='withdraw_cbe_bank')],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]
    ]
    return InlineKeyboardMarkup(keyboard)
   




async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = withdraw_opitions_keyboard()  # Create the inline keyboard
    await update.message.reply_text("Choose a withdraw method", reply_markup=reply_markup)


async def get_withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text
    # Get user's wallet balance
    user_id = update.effective_user.id
 
    try:
        wallet_response = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/').json()
        balance = wallet_response.get('balance', 0)

        
        # Check if withdrawal amount exceeds balance
        if float(amount) > float(balance):

            await update.message.reply_text(f"Insufficient funds. Your current balance is {balance} ETB")
            return WITHDRAW_AMOUNT_CONFIRM

        else:
            # Store amount in context for later use
            context.user_data['withdraw_amount'] = amount
            
            await update.message.reply_text(
                "Please enter your Telebirr number or bank account number where you want to receive the withdrawal:"
            )
            return GET_WITHDRAW_ACCOUNT

        
    except Exception as e:
        logger.error(f"Error checking wallet balance: {e}")
        await update.message.reply_text("Error checking your balance. Please try again later.")
        return ConversationHandler.END
  
        
  
    

   

    



async def get_withdraw_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    account_number = update.message.text
    BACK_URL = "https://api.bilenbingo.com"
    admin_message = (
        f"New withdrawal request:\n"
        f"User: {update.effective_user.username}\n" 
        f"Account: {account_number}"
    )
    try:
        print("url data ",f'{BACK_URL}/support/payment-requests/')
        response = requests.post(f'{BACK_URL}/support/payment-requests/', data={
            'user': update.effective_user.id,
            'amount': context.user_data['withdraw_amount'],
            'account_number': account_number,
            'status': 'pending'
        }, headers={'Referer': BACK_URL})
        print("response = ",response.json())

        if response.status_code == 200:
            response = requests.post(f'{BACK_URL}/payments/withdrawal-request/', json={
                'user_id': update.effective_user.id,
                'amount': context.user_data['withdraw_amount'],
                'account_number': account_number
            })
            print("response = ",response.json())
            await update.message.reply_text("Your withdrawal request has been submitted. We will process it shortly.")
        else:
            await update.message.reply_text("Failed to create payment request")
        if response.status_code == 403:
            raise Exception("Failed to create payment request")

            
        # await context.bot.send_message(chat_id=7689314790, text=admin_message)
        await context.bot.send_message(chat_id=7816837214, text=f"🔔 *New Withdrawal Request*\n\n👤 *User:* {update.effective_user.username}\n💰 *Amount:* {context.user_data['withdraw_amount']} ETB\n🏦 *Account:* {account_number}\n⏳ *Status:* Pending")
       
        
     
        await update.message.reply_text("Your withdrawal request has been submitted. We will process it shortly.")
    except Exception as e:
        logger.error(f"Error sending admin notification: {e}")
        await update.message.reply_text(f"{e}")
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
        [InlineKeyboardButton("📞 Support",  url='https://t.me/BilenSupport')],
    ]
    return InlineKeyboardMarkup(keyboard)



async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = support_options_keyboard()
    await update.message.reply_text("Contact us using support button. We will respond to your message as soon as possible.", reply_markup=reply_markup)



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
                f"https://www.bilenbingo.com/?playerId={player_id}&name={username}&betAmount={bet_amount}&wallet_amount={balance}"
            )
            print("web_app_url = ",web_app_url)
        if query.data == 'play_demo':
            player_id = query.from_user.id
            username = query.from_user.username
            user_id = query.from_user.id
            bet_amount = 0  # Demo game has no bet amount
            wallet_amount = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/').json().get('balance',0)
            web_app_url = (
                f"https://www.bilenbingo.com/?playerId={player_id}&name={username}&betAmount={bet_amount}&wallet_amount={wallet_amount}&demo=true"
            )

            print("web_app_url = ",web_app_url)
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

        elif query.data == 'contact_support':
            await query.edit_message_text(
                text="Choose a contact support:",
                reply_markup=support_options_keyboard()
            )

            


        elif query.data == 'play_instruction':
            chat_id = update.effective_chat.id
            local_video_path = './assets/play.mp4'
            caption = 'play instruction!'

            with open(local_video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file, caption=caption)

        elif query.data == 'get_deposit_amount':
          
            return DEPOSIT_AMOUNT

        elif query.data == "withdraw_telebirr":
            await query.edit_message_text(
                text="how much do you want to withdraw?")
            
            return WITHDRAW_AMOUNT_CONFIRM

        elif query.data == "withdraw_cbe_bank":
            await query.edit_message_text(
                text="how much do you want to withdraw?")
            
            return WITHDRAW_AMOUNT_CONFIRM

            
            
       
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
                "• Manual Deposit\n\n"
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
                f"https://www.bilenbingo.com/?playerId={player_id}&name={username}&betAmount={bet_amount}&wallet_amount={wallet_amount}"
            )

            keyboard = [
                [InlineKeyboardButton("Open Bilen Bingo!", web_app=WebAppInfo(url=web_app_url))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text("Start playing Bilen bingo", reply_markup=reply_markup)

        elif query.data == 'deposit':
            keyboard = [
                [
                 InlineKeyboardButton("Telebirr", callback_data='get_deposit_amount_of_telebirr'),
                 InlineKeyboardButton("CBE Bank", callback_data='get_deposit_amount_of_cbe_bank')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
          
            await query.edit_message_text(text="Please select deposit method:", reply_markup=reply_markup)

        elif query.data == 'get_deposit_amount_of_telebirr':

            await query.edit_message_text(
                text="Please enter your deposit amount in this format:"
            )
            return DEPOSIT_AMOUNT

        elif query.data == 'get_deposit_amount_of_cbe_bank':
            await query.edit_message_text(
                text="Please enter your deposit amount in this format:"
            )
            return DEPOSIT_AMOUNT
          
          
            
        

       

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
            await query.edit_message_text("Welcome to Bilen Bingo! Please select an option:", reply_markup=reply_markup)
            
            
 
        else:

            keyboard = [
                [InlineKeyboardButton("Play Game", callback_data='play'),
                 InlineKeyboardButton("Check Balance", callback_data='check_balance')],
                [InlineKeyboardButton("Deposit", callback_data='deposit'),
                 InlineKeyboardButton("Register", callback_data='register')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Welcome to Bilen Bingo! Please select an option:", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error handling query: {query.data} - {e}")
        await query.edit_message_text(text="An error occurred. Please try again.")

async def deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "እባክዎ ክፍያውን ከሚከተሉት መለያዎች ወደ አንዱ ያስተላልፉ፡-\n"
        "📱 ቴሌብር፡ 0927832338\n"
        "🏦 ንግድ ባንክ፡ 1000095634037\n"
        "ከከፈሉ በኋላ ከባንክ ወይም ከቴሌቢር የደረሰዎትን የማረጋገጫ መልእክት ላኩልን።"
    )

    return GET_TRANSCATION_DETAILS
  

    




async def get_transcation_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  
    message = update.message.text
    BACK_URL = "https://api.bilenbingo.com"
    try:
        # Extract amount using regex
        import re
        # Find amount pattern "ETB X.XX" or "ETB X"
        amount_match = re.search(r'ETB\s+(\d+(?:\.\d{2})?)', message)
        amount = amount_match.group(1) if amount_match else None

        # Find transaction number after "transaction number is"
        transaction_match = re.search(r'transaction number is (\w+)', message)
        transaction_number = transaction_match.group(1) if transaction_match else None
        print("transaction_match = ",amount)
        print("transaction_number = ",transaction_number)
        data = {
            "user_id": update.effective_user.id,
            "username": update.effective_user.username,
            "amount": amount,
            "transaction_number": transaction_number
        }

        print("url data ",f'{BACK_URL}/payments/deposit/')
        response = requests.post(f'{BACK_URL}/payments/deposit/', json=data)
    
        if response.status_code == 200:
            await update.message.reply_text(f"{response.json().get('message')}")
        else:
            await update.message.reply_text(f"{response.json().get('message')}")

        if not amount or not transaction_number:
            raise ValueError("Could not extract transaction details")
        await update.message.reply_text(f"Amount: {amount} ETB\nTransaction number: {transaction_number}")
    except Exception as e:
        logger.error(f"Error extracting transaction details: {e}")
        await update.message.reply_text("Could not process transaction details. Please contact support.")

      
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
        "withdraw", 
        "withdraw funds"
        ),
    BotCommand(
        "invite", 
        "Invite your friends"
        )
    ]


async def post_init(app):
    await app.bot.set_my_commands(all_public_commands_descriptions)


      
  

async def handle_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    BACK_URL = "https://api.bilenbingo.com/"
    
    # Check if user is registered
    response = requests.get(f'{BACK_URL}/accounts/filter-users/{user_id}/')
    if response.status_code != 200:
        await update.message.reply_text(
            "You need to register first before inviting others. Use the /register command."
        )
        return

    # Get user's wallet balance
    wallet_response = requests.get(f'{BACK_URL}/payments/wallet/{user_id}/').json()
    balance = wallet_response.get('balance', 0)

    invite_link = f"https://t.me/bilanbingobot?start={user_id}"
    
    message = (
        f"🎮 Invite your friends to Bilen Bingo!\n\n"
        f"Share this link with your friends:\n{invite_link}\n\n"
        f"Your current balance: {balance} ETB\n\n"
        f"Invite friends and enjoy playing together! 🎲"
    )

    # Add 20 ETB bonus for inviting
    requests.post(f'{BACK_URL}/payments/wallet/add-balance/', json={
        'user_id': user_id,
        'amount': 20
    })
    
    await update.message.reply_text(message)



def main() -> None:
    # application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    application = ApplicationBuilder().token("7774913647:AAGx1yP7Puq1TXRdpsa6dMxbZsiS1yXZiJ0").post_init(post_init).build()
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
            # get_deposit_amount
            DEPOSIT_AMOUNT          : [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount)],
            GET_WITHDRAW_ACCOUNT    : [MessageHandler(filters.TEXT & ~filters.COMMAND, get_withdraw_account)],
            WITHDRAW_AMOUNT_CONFIRM : [MessageHandler(filters.TEXT & ~filters.COMMAND, get_withdraw_amount)],
            GET_TRANSCATION_DETAILS  : [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transcation_details)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

  
 

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('play', play_command))
    # application.add_handler(CommandHandler("deposit",deposit_command))
    application.add_handler(CommandHandler('instructions', instruction_command))
    application.add_handler(CommandHandler('support', support_command))
    application.add_handler(CommandHandler('withdraw', withdraw_command))
    application.add_handler(deposit_conversation_handler)
    # application.add_handler(CommandHandler('broadcast', broadcast_message))
    application.add_handler(CommandHandler('invite', handle_invite))  
    # application.add_handler(withdraw_conversation_handler)
    application.add_handler(register_conversation_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

async def conversation_timeout(context):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text="Conversation timed out due to inactivity. Please start again."
    )
    # Optionally, reset any user data here

async def cancel(update, context):
    await update.message.reply_text("Conversation cancelled. You can start again anytime.")
    return ConversationHandler.END