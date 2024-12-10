from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import TelegramUser
from .models import Wallet
# Create your views here.

import math

def get_balance(request):
    username = request.GET.get('username')
   
    try:
        telegram_user = TelegramUser.objects.filter(username=username).first()
        wallet = Wallet.objects.get(user=telegram_user)
        return JsonResponse({
            'balance': float(round(wallet.balance, 2) )
        })
    except (TelegramUser.DoesNotExist, Wallet.DoesNotExist):
        return JsonResponse({'error': 'Wallet not found'}, status=404)
    
def success(request):
    
    # Get payment data from POST request
    data = request.POST
    username = data.get('username')
    amount = float(data.get('amount', 0))

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
    return JsonResponse({'message': 'Payment successful'})

def error(request):
    data = request.POST
    username = data.get('username')
    amount = float(data.get('amount', 0))   
    print("username = ",username)
    print("amount = ",amount)
    print("data = ",data)
    print("request = ",request)
    return JsonResponse({'message': 'Payment failed'})
