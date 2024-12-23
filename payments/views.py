from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import TelegramUser
from .models import Wallet
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
        phone =  "251921309013" # telegram_user.phone
        response = requests.get(f"https://uat.api.addispay.et/merchant/customer/transactions?phone={phone}",headers=headers)
        print("response = ",response.text)
    
        wallet = response.json()
        print("wallet = ",wallet)
        if wallet != None:
            return JsonResponse({'balance': wallet.get('data')})
            return JsonResponse({'error': 'Wallet balance is negative'}, status=400)    
    except (TelegramUser.DoesNotExist, Wallet.DoesNotExist):
        return JsonResponse({'error': 'Wallet not found'}, status=404)
    

@csrf_exempt
def get_wallet(request,username):
    telegram_user = TelegramUser.objects.filter(username=username).first()
    wallet = Wallet.objects.filter(user=telegram_user).first()
    if wallet is None:
        wallet = wallet.balance
        return JsonResponse({'balance': wallet})
    else:
        wallet = 0
        return JsonResponse({'balance': wallet})





@csrf_exempt
def success(request):
    data = json.loads(request.body)
    
    username = data.get('order').get('username', '')  # Note: keeping the typo from the data structure
    amount = float(data.get('order').get('amount', 0))

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
    # data =  { 
    #         'session_uuid': '8d09c5e9-73b4-44b9-92d1-97d580edf5b1',
    #           'addispay_transaction_id': 'ADP-ZZIHO1XRKS', 'third_party_transaction_ref': 'BLN4WCRV6Q', 
    #           'total_amount': 30.3, 'paymnet_reason': 'Process service request successfully.', 
    #           'payment_status': 'success', 
    #           'order_id': 'selam_pay_W)=tX:Bg6TS#,a#F3(."w0S:(ej;{jMWyLsl==TR!FzFxzbmxbBqL)v2YZD[,:CF', 'nonce': 'ADP-ZZIHO1XRKS',
    #          'order': {'items': 'single bot transcation', 'amount': 30.0, 'username': 'ThreeWaybetYourchoice', 'description': 'the transcationt to deposit amount in my bot wallet', 'phoneNumber': '251911992283', 'telecomOperator': 'ethio_telecom'}}

    # Get username and amount from data
    username = data.get('order').get('username', '')  # Note: keeping the typo from the data structure
    amount = float(data.get('order').get('amount', 0))

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


