from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import TelegramUser
from .models import Wallet,Commission
from django.views.decorators.csrf import csrf_exempt
import requests
# Create your views here.


# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwaG9uZU51bWJlciI6IjI1MTk0Mzk0NjAzNCIsInVzZXJfaWQiOjQ5LCJleHAiOjE3MzUxMjI0NzF9.iVD899bRHtAMUHQkf4_E0kSXeLCIY0cuAWbSNL4zdvM

import math
import json
@csrf_exempt
def get_balance(request):
    username = request.GET.get('username',"")
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwaG9uZU51bWJlciI6IjI1MTk5MTIyMTkxMiIsInVzZXJfaWQiOjI5LCJleHAiOjE3MzUyMDU4ODF9.mFHDjXUe9ZKQ-aS1fNgp2HfQUDKPbLyjRmamzFNjCIA"
    }
    if username == "":
        return JsonResponse({'error': 'Username is required'}, status=400)
   
    try:
        telegram_user = TelegramUser.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(user=telegram_user).first()
        if wallet != None:
            return JsonResponse({'balance': wallet.balance})
        else:
            return JsonResponse({'error': 'Wallet balance is negative'}, status=400)    
    except (TelegramUser.DoesNotExist, Wallet.DoesNotExist):
        return JsonResponse({'error': 'Wallet not found'}, status=404)
    

@csrf_exempt
def get_wallet(request,username):
    telegram_user = TelegramUser.objects.filter(username=username).first()
    wallet = Wallet.objects.filter(user=telegram_user).first()
    if wallet is not None:
        wallet = wallet.balance
        return JsonResponse({'balance': wallet})
    else:
        wallet = 0
        return JsonResponse({'balance': wallet})





@csrf_exempt
def success(request):
    print("success = ",request.body)
    data = json.loads(request.body)
    
    username = data.get('order').get('username', '')  # Note: keeping the typo from the data structure
    amount = float(data.get('order').get('amount', 0))
    print("username from addispay = ",username)
    print("amount from addispay = ",amount)

    try:
        # Get or create user wallet
        telegram_user = TelegramUser.objects.filter(username=username).first()
        wallet, created = Wallet.objects.get_or_create(user=telegram_user)
        
        # Add payment amount to wallet balance
        wallet.balance += amount
        wallet.save()

        return JsonResponse({
            'success': True,
            'message': 'Payment processed successfully',
            'new_balance': float(wallet.balance)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
   
@csrf_exempt
def error(request):
    data = json.loads(request.body)
  
    
    return JsonResponse({'message': 'Payment Failed'})
  


@csrf_exempt
def win(request):
    # Get payment data from POST request
    data = json.loads(request.body)
    username = data.get('username','')
    if username == "":
        return JsonResponse({'message': 'Username is required'}, status=400)
    amount = data.get('amount',0.0)
 

    try:
        # Get or create user wallet
        telegram_user = TelegramUser.objects.filter(username=username).first()
        print("telegram_user = ",telegram_user)
        wallet, created = Wallet.objects.get_or_create(user=telegram_user)
        print("wallet = ",wallet)
        print("created = ",created)
        
        # Add winning amount to wallet balance
        wallet.balance += float(amount)
        wallet.save()

        return JsonResponse({
            'success': True,
            'message': 'Win amount added successfully',
            'new_balance': float(wallet.balance)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
def withdraw(request):
    data = json.loads(request.body)
    username = data.get('username','')
    if request.method == "POST":
        if username == "":
            return JsonResponse({'message': 'Username is required'}, status=400 )
        amount = data.get('amount',0.0)
        if amount == 0.0:
            return JsonResponse({'message': 'Amount is required'}, status=400)
        telegram_user = TelegramUser.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(user=telegram_user).first()
        wallet.balance -= float(amount)
        wallet.save()
        return JsonResponse({'message': 'Withdrawal successful'})
    else:
        telegram_user = TelegramUser.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(user=telegram_user).first()
        return JsonResponse({'balance': wallet.balance})


@csrf_exempt
def loss(request):
    data = json.loads(request.body)
    username = data.get('username','')
    if username == "":
        return JsonResponse({'message': 'Username is required'}, status=400)
    
    amount = data.get('amount',0.0) 
    try:
        telegram_user = TelegramUser.objects.filter(username=username).first()
        wallet = Wallet.objects.filter(user=telegram_user).first()
        wallet.balance -= float(amount)
        wallet.save()
        return JsonResponse({'message': 'Loss done'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)



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
def withdraw_success(request):
    print("withdraw_success = ",request.body)
    data = json.loads(request.body)

    username = data.get('username','')
    if username == "":
        return JsonResponse({'message': 'Username is required'}, status=400)
    amount = data.get('amount',0.0)
    if amount == 0.0:

        return JsonResponse({'message': 'Amount is required'}, status=400)
    telegram_user = TelegramUser.objects.filter(username=username).first()
    wallet = Wallet.objects.filter(user=telegram_user).first()
    wallet.balance += float(amount)
    wallet.save()
   
    return JsonResponse({'message': 'Withdrawal successful'})

@csrf_exempt
def withdraw_error(request):
   
    return JsonResponse({'message': 'Withdrawal failed'})



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