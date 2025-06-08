from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import TelegramUser
from .models import Wallet,Commission,Charge,WinTracker,PaymentSession,DepositMessage
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import requests
# Create your views here.


# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwaG9uZU51bWJlciI6IjI1MTk0Mzk0NjAzNCIsInVzZXJfaWQiOjQ5LCJleHAiOjE3MzUxMjI0NzF9.iVD899bRHtAMUHQkf4_E0kSXeLCIY0cuAWbSNL4zdvM

import math
import json
@csrf_exempt
def get_balance(request):
    user_id = request.GET.get('user_id',0)
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwaG9uZU51bWJlciI6IjI1MTk5MTIyMTkxMiIsInVzZXJfaWQiOjI5LCJleHAiOjE3MzUyMDU4ODF9.mFHDjXUe9ZKQ-aS1fNgp2HfQUDKPbLyjRmamzFNjCIA"
    }
    if user_id == 0:
        return JsonResponse({'error': 'User id is required'}, status=400)
   
    try:
        telegram_user = TelegramUser.objects.filter(telegram_id=user_id).first()
        wallet = Wallet.objects.filter(user=telegram_user).first()
        if wallet != None:
            return JsonResponse({'balance': wallet.balance})
        else:
            return JsonResponse({'error': 'Wallet balance is negative'}, status=400)    
    except (TelegramUser.DoesNotExist, Wallet.DoesNotExist):
        return JsonResponse({'error': 'Wallet not found'}, status=404)
    

@csrf_exempt
def get_wallet(request,user_id):
    telegram_user = TelegramUser.objects.filter(telegram_id=user_id).first()
    wallet = Wallet.objects.filter(user=telegram_user).first()  
    if wallet is not None:
        wallet = wallet.balance
        return JsonResponse({'balance': wallet})
    else:
        wallet = 0
        return JsonResponse({'balance': wallet})





@csrf_exempt
def success(request):
    
    data = json.loads(request.body)
    print("data = ",data)   
    session_id = data.get('sessionId','')
    if session_id == "":
        return JsonResponse({'message': 'Session id is required'}, status=400)
    payment_session = PaymentSession.objects.filter(session_id=session_id).first()

    try:
        telegram_user = TelegramUser.objects.get(telegram_id=payment_session.user.telegram_id)
    except TelegramUser.DoesNotExist:
        return JsonResponse({'message': 'Telegram user not found'}, status=404)

    if payment_session is None:
        return JsonResponse({'message': 'Payment session not found'}, status=404)
    if data.get('transactionStatus') == "SUCCESS":
        payment_session.status = "paid"
        payment_session.save()



        bot_token = "7955523403:AAEavfPGnqIhCT452qlpydrtmicxkiK_wzc"
        chat_id = telegram_user.telegram_id

        message = f"✅ *Payment Successful!*\n\n💰 Amount: *{payment_session.amount} ETB*\n\nThank you for your payment! 🙏"
        
        
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        wallet = Wallet.objects.filter(user=telegram_user).first()
        if wallet is not None:
            wallet.balance += float(payment_session.amount)
            wallet.save()
        requests.post(telegram_url, json=payload)

    else:
        bot_token = "7955523403:AAEavfPGnqIhCT452qlpydrtmicxkiK_wzc"
        chat_id = telegram_user.telegram_id
        payment_session.status = "failed"
        payment_session.save()

        message = f"❌ *Payment Failed*\n\n💰 Amount: *{payment_session.amount} ETB*\n\nPlease try again or contact support if the issue persists."
        
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(telegram_url, json=payload)
        return JsonResponse({'message': 'Payment session updated successfully'})
   



    
   
@csrf_exempt
def error(request):
    data = json.loads(request.body)
    session_id = data.get('sessionId')
    payment_session = PaymentSession.objects.filter(session_id=session_id).first()
    
    if not payment_session:
        return JsonResponse({'message': 'Payment session not found'}, status=404)
        
    payment_session.status = "failed"
    payment_session.save()
    
    try:
        bot_token = "7955523403:AAEavfPGnqIhCT452qlpydrtmicxkiK_wzc"
        chat_id = payment_session.user.telegram_id

        message = f"❌ *Payment Failed*\n\n💰 Amount: *{payment_session.amount} ETB*\n\nPlease try again or contact support if the issue persists."
        
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        requests.post(telegram_url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")

  
    
    return JsonResponse({'message': 'Payment Failed'})
  


@csrf_exempt
def win(request):
    # Get payment data from POST request

        #  playerId,
        # amount ,
        # gameId
    data = json.loads(request.body)
    user_id = data.get('playerId','')
    game_id = data.get('gameId','')
    amount = data.get('amount',0.0)
    if user_id == "":
        return JsonResponse({'message': 'User id is required'}, status=400)
    if game_id == "":
        return JsonResponse({'message': 'Game id is required'}, status=400)
    if amount == "":
        return JsonResponse({'message': 'Amount is required'}, status=400)

    try:
        player = TelegramUser.objects.get(telegram_id=user_id)
    except TelegramUser.DoesNotExist:
        return JsonResponse({'message': 'Player not found'}, status=404)

    if player is None:
        return JsonResponse({'message': 'Player not found'}, status=404)
    
    win_tracker = WinTracker.objects.filter(game_id=game_id).first()

 
    if win_tracker is not None:
        return JsonResponse({'message': f'Player already won this game {game_id} '}, status=400)
    else:
        wallet = Wallet.objects.get(user=player)
        wallet.balance += float(amount)
        win_tracker = WinTracker.objects.create(user=player, game_id=game_id, win_amount=float(amount))
        wallet.save()
        return JsonResponse({'message': f'Win amount {amount} added to {player.username} successfully'})





    


@csrf_exempt
def withdraw(request):
    if request.method != "POST":
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
    data = json.loads(request.body)
    user_id = data.get('userId')
    amount = data.get('amount')

    if user_id == "":
        return JsonResponse({'message': 'User id is required'}, status=400)
    if amount == "":
        return JsonResponse({'message': 'Amount is required'}, status=400)
    try:
        telegram_user = TelegramUser.objects.get(telegram_id=user_id)
        wallet = Wallet.objects.get(user=telegram_user)
        wallet.balance -= float(amount)
        wallet.save()
        return JsonResponse({'message': 'Withdrawal successful'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@csrf_exempt
def loss(request):
    data = json.loads(request.body)
    playersInGame = data.get('players', [])
    betAmount = data.get('betAmount', 0.00)
    gameId = data.get('gameId', '')

    charged_players = []
    skipped_players = []

    for player_data in playersInGame:
        player = TelegramUser.objects.get(telegram_id=player_data.get('playerId'))
        if player is None:
            print(f"Player {player_data.get('playerId')} not found.")
            continue  

        existing_charge = Charge.objects.filter(game_id=gameId, player=player, charged=True).first()
        if existing_charge is not None:
            print(f"Player {player.telegram_id} already charged for game {gameId}.")
            skipped_players.append(player)
            continue

        with transaction.atomic():
            wallet = Wallet.objects.get(user=player)
            if wallet is None:
                print(f"Wallet not found for player {player.telegram_id}.")
                skipped_players.append(player)
                continue

            if wallet.balance < float(betAmount):
                print(f"Insufficient balance for player {player.telegram_id}. Balance: {wallet.balance}, Bet: {betAmount}.")
                skipped_players.append(player)
                continue

            wallet.balance -= float(betAmount)
            wallet.save()
            Charge.objects.create(game_id=gameId, betAmount=float(betAmount), player=player, charged=True)
            charged_players.append(player)

    if charged_players:
        return JsonResponse({'message': 'Charges processed', 'charged': len(charged_players), 'skipped': len(skipped_players)})
    else:
        return JsonResponse({'message': 'No charges processed, all players already charged or skipped.'})



@csrf_exempt
def commission(request):
    data = json.loads(request.body)

    game_type = data.get('game_type')
    if game_type == "": 
        return JsonResponse({'message': 'Game type is required'}, status=400)
    amount = data.get('amount')
    if amount == "":
        return JsonResponse({'message': 'Amount is required'}, status=400)
    commission = Commission.objects.create(game_type=game_type, amount=amount)
    return JsonResponse({'message': 'Commission created successfully'})




@csrf_exempt
def return_funds(request):
    if request.method != "POST":
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
    data = json.loads(request.body)
    print("data = ",data)
    username = data.get('username')
    if username == "":  
        return JsonResponse({'message': 'Username is required'}, status=400)
    amount = data.get('betAmount',0.0)
    if amount == 0.0:
        return JsonResponse({'message': 'Amount is required'}, status=400)
    try:
        telegram_user = TelegramUser.objects.filter(username=username).first()
        print("telegram_user = ",telegram_user)
        wallet = Wallet.objects.filter(user=telegram_user).first()
        print("wallet = ",wallet)
        print("amount = ",amount)
        wallet.balance += float(amount)
        wallet.save()
        return JsonResponse({'message': 'Funds returned successfully'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    


@csrf_exempt
def create_payment_session(request):
    data = json.loads(request.body)
    print("data = ",data)
    user_id = data.get('user_id',0)
    amount = data.get('amount',0.0)
    reference_no = data.get('reference_no','')
    payment_id = data.get('payment_id','default')
    session_id = data.get('session_id','default')
    status = data.get('status','')
    telegram_user = TelegramUser.objects.filter(telegram_id=user_id).first()
    if telegram_user is None:
        return JsonResponse({'message': 'User not found'}, status=404)

    payment_session = PaymentSession.objects.create(
        user=telegram_user,
        amount=amount,
        reference_no=reference_no,
        session_id=session_id,
        status=status
    )
    return JsonResponse({'message': 'Payment session created successfully'},status=201)





@csrf_exempt
def notify_url(request):
    print("notify_url = ",request.body)
    data = json.loads(request.body)
    print("data = ",data)
   
    session_id = data.get('sessionId','')
    payment_session = PaymentSession.objects.get(session_id=session_id)
    if payment_session is None:
        return JsonResponse({'message': 'Payment session not found'}, status=404)
    payment_session.status = data.get('transactionStatus','')
    if payment_session.status == "SUCCESS":
        wallet = Wallet.objects.get(user=payment_session.user)
        wallet.balance += float(payment_session.amount)
        wallet.save()

    # Notify user via Telegram about transaction status
    bot_token = "6968354140:AAHc2VCRTibuuOnvqOHJDcsWXA7sJMpJ8ww"
    chat_id = payment_session.user.telegram_id
    if payment_session.status == "SUCCESS":
        message = f"✅ Payment Successful!\nAmount: {payment_session.amount} ETB has been added to your wallet."
    else:
        message = f"❌ Payment Failed!\nTransaction Status: {payment_session.status}"
        
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    requests.post(telegram_url, json=payload)
    payment_session.status = data.get('transactionStatus','')
    payment_session.save()
    return JsonResponse({'message': 'Payment session updated successfully'})




@csrf_exempt
def notify_url_withdraw(request):
    return JsonResponse({'message': 'Withdrawal successful'})
    
   
    



@csrf_exempt
def deposit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("data = ",data)
        user_id = data.get('user_id',0)
        amount = data.get('amount',0.0)
        transaction_number = data.get('transaction_number','')
        
        # Check if transaction number already exists
        existing_deposit = DepositMessage.objects.filter(transaction_number=transaction_number).first()
        print("existing_deposit = ",existing_deposit)
        if existing_deposit is None:
            return JsonResponse({'message': 'Transaction number does not exist'})
    
        telegram_user = TelegramUser.objects.filter(telegram_id=user_id).first()
        if telegram_user is None:
            return JsonResponse({'message': 'User not found'})
        wallet = Wallet.objects.get(user=telegram_user)
        wallet.balance += existing_deposit.amount
        wallet.save()
        existing_deposit.delete()
        return JsonResponse({'message': 'Deposit successful'})


@csrf_exempt
def deposit_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get('message','')
        import re
        
        # Find amount pattern "ETB X.XX" or "ETB X"
        amount_match = re.search(r'ETB\s+(\d+(?:\.\d{2})?)', message)
        amount = float(amount_match.group(1)) if amount_match else 0.0

        # Find transaction number after "transaction number is"
        transaction_match = re.search(r'transaction number is (\w+)', message) 
        transaction_number = transaction_match.group(1) 

        if not amount or not transaction_number:
            return JsonResponse({'error': 'Could not extract transaction details'}, status=400)
    
       
        DepositMessage.objects.create(message=message, amount=amount, transaction_number=transaction_number)
        return JsonResponse({'message': 'Deposit message created successfully'})
    else:
        message = []
        for message in DepositMessage.objects.all():    
            message.append({
                'message': message.message,
                'amount': message.amount,
                'transaction_number': message.transaction_number
            })
        return JsonResponse({'message': message}, status=200)

