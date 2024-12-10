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
    