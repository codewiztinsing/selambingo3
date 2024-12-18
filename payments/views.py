from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import TelegramUser
from .models import Wallet
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import math
import json
@csrf_exempt
def get_balance(request):
    username = request.GET.get('username',"")
    if username == "":
        return JsonResponse({'error': 'Username is required'}, status=400)
   
    try:
        telegram_user = TelegramUser.objects.filter(username=username).first()
        wallet = Wallet.objects.get(user=telegram_user)
        if wallet.balance != None:
           
            return JsonResponse({
                'balance': float(round(wallet.balance, 2) )
            })
        else:
            return JsonResponse({'error': 'Wallet balance is negative'}, status=400)    
    except (TelegramUser.DoesNotExist, Wallet.DoesNotExist):
        return JsonResponse({'error': 'Wallet not found'}, status=404)
    
@csrf_exempt
def success(request):
    
    # Get payment data from POST request
    data = request.body
    data = json.loads(data)

    print("data = ",data)
    username = data.get('order_detail').get('username')
    print("username = ",username)
    amount = float(data.get('order_detail').get('amount', 0))
    print("amount = ",amount)

    try:
        # Get or create user wallet
        telegram_user = TelegramUser.objects.filter(username=username).first()
        print("telegram_user = ",telegram_user)
        wallet, created = Wallet.objects.get_or_create(user=telegram_user)
        print("wallet = ",wallet)
        print("created = ",created)
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
    return JsonResponse({'message': 'Payment successful'})
@csrf_exempt
def error(request):
    data = request.POST
    username = data.get('username')
    amount = float(data.get('amount', 0))   
    print("username = ",username)
    print("amount = ",amount)
    print("data = ",data)
    print("request = ",request)
    return JsonResponse({'message': 'Payment failed'})


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
    return JsonResponse({'message': 'Payment successful'})

@csrf_exempt
def withdraw(request):
    data = json.loads(request.body)
    username = data.get('username')
    amount = data.get('amount')
    return JsonResponse({'message': 'Withdrawal successful'})


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


