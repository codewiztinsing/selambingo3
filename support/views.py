from django.shortcuts import render
from accounts.models import TelegramUser, User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from .models import PaymentRequest, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from payments.models import Wallet
import json

def support_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("username = ",username)
        print("password = ",password)
        password = password
        print("password = ",password)
     
        user = authenticate(request, username=username, password=password)  
    
        if user is not None and user.check_password(password):
            login(request, user)
            if user.is_superuser:
                return redirect('support:admin_dashboard')
            else:
                return redirect('support:support_dashboard')

        else:
            return render(request, 'support/login.html', {'message': 'Invalid username or password'})
    return render(request, 'support/login.html')

    
@login_required(login_url='support:support_login')
def support_dashboard(request):
    payment_requests = PaymentRequest.objects.all()
    print("payment_requests = ",payment_requests)
    return render(request, 'support/dashboard.html', {'payment_requests': payment_requests})


@csrf_exempt
def payment_requests(request):
    all_payment_requests = PaymentRequest.objects.all()
    payment_requests = []
    if request.method == 'POST':
        print("request.POST = ",request.POST['user'])
        telegram_user = TelegramUser.objects.filter(telegram_id=request.POST['user']).first()
        print("telegram_user = ",telegram_user)
        if telegram_user:
            amount = request.POST['amount']
            status = request.POST['status']
            account_number = request.POST['account_number'] 
            payment_request = PaymentRequest.objects.create(user=telegram_user, amount=amount, status=status, account_number=account_number)
            return JsonResponse({'message': 'Payment request created successfully'})
        else:
            return JsonResponse({'message': 'Telegram user not found'}, status=404)


    all_payment_requests = all_payment_requests.order_by('-created_at')

    for payment_request in all_payment_requests:
        payment_requests.append({
            'id': payment_request.id,
            'account_number': payment_request.account_number,
            'user': payment_request.user.id,
            'amount': payment_request.amount,
            'status': payment_request.status
        })
    
    return JsonResponse({'payment_requests': payment_requests}, status=200)



def approve_withdrawal(request, id):
    payment_request = PaymentRequest.objects.get(id=id)
    payment_request.status = 'approved'
    payment_request.save()
    return JsonResponse({'message': 'Withdrawal approved successfully'})


def reject_withdrawal(request, id):
    body = request.body
    data = json.loads(body)
    username = data.get('username')
    print("username = ",username)
    amount = data.get('amount')
    print("amount = ",amount)
    payment_request = PaymentRequest.objects.get(id=id)
    print("payment_request = ",payment_request)
    wallet = Wallet.objects.get(user=payment_request.user)
    print("wallet = ",wallet)
    wallet.balance += float(amount)
    print("wallet.balance = ",wallet.balance)
    wallet.save()
    print("wallet.save() = ",wallet.save())
    payment_request.delete()
   
    return JsonResponse({'message': 'Withdrawal rejected successfully'})



@login_required(login_url='support_login')
def admin_dashboard(request):
    # Get all data from different models
    telegram_users = TelegramUser.objects.all()
    payment_requests = PaymentRequest.objects.all()
    
    # Format data for template
    users_data = []
    for user in telegram_users:
        users_data.append({
            'id': user.id,
            'telegram_id': user.telegram_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            # 'balance': user.balance,
            'created_at': user.created_at,
        
        })
    total_users = len(users_data)

    payments_data = []
    for payment in payment_requests:
        payments_data.append({
            'id': payment.id,
            'user': payment.user.username,
            'amount': payment.amount,
            'account_number': payment.account_number,
            'status': payment.status,
            'created_at': payment.created_at
        })
    total_payments = len(payments_data)
    total_revenue = sum(payment.amount for payment in payment_requests)

    context = {
        'users': users_data,
        'payments': payments_data,
        'total_users': total_users,
        'total_payments': total_payments,
        'total_revenue': total_revenue
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        model_type = request.POST.get('model_type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = first_name + last_name + '@gmail.com'
        password = request.POST.get('password')
        username = request.POST.get('username')
        if action == 'create':
            try:
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_superuser=False,
                    is_staff=True,
                    is_active=True
                )
                user.set_password(password)
                user.save()
                return JsonResponse({'message': 'User created successfully'})
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)
                

        elif action == 'update':
            item_id = request.POST.get('id')
            if model_type == 'user':
                user = TelegramUser.objects.get(id=item_id)
                user.username = request.POST.get('username', user.username)
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.phone = request.POST.get('phone', user.phone)
                user.balance = request.POST.get('balance', user.balance)
                user.save()
                return JsonResponse({'message': 'User updated successfully'})
            
            elif model_type == 'payment':
                payment = PaymentRequest.objects.get(id=item_id)
                payment.status = request.POST.get('status', payment.status)
                payment.save()
                return JsonResponse({'message': 'Payment updated successfully'})

        elif action == 'delete':
            item_id = request.POST.get('id')
            if model_type == 'user':
                TelegramUser.objects.filter(id=item_id).delete()
                return JsonResponse({'message': 'User deleted successfully'})
            
            elif model_type == 'payment':
                PaymentRequest.objects.filter(id=item_id).delete()
                return JsonResponse({'message': 'Payment deleted successfully'})

        return JsonResponse({'message': 'Invalid action'}, status=400)

    return render(request, 'support/admin_dashboard.html', context)



def transcations(request):
    transcations = Transaction.objects.all()
    transcations_data = []
    for transcation in transcations:
        transcations_data.append({
            'id': transcation.id,
            'user': transcation.user.username,
            'amount': transcation.amount,
        })
    total_transcations = len(transcations_data)
    total_approved_transcations = len(transcations_data.filter(status='approved'))
    total_pending_transcations = len(transcations_data.filter(status='pending'))
    total_rejected_transcations = len(transcations_data.filter(status='rejected'))
    total_revenue = sum(transcations_data.filter(status='approved').values_list('amount', flat=True))
    return render(request, 'support/transcations.html', {'transcations': transcations_data, 'total_transcations': total_transcations, 'total_approved_transcations': total_approved_transcations, 'total_pending_transcations': total_pending_transcations, 'total_rejected_transcations': total_rejected_transcations, 'total_revenue': total_revenue})

def reports(request):
    transcations = Transaction.objects.all()
    total_transcations = len(transcations)
    total_approved_transcations = len(transcations.filter(status='approved'))
    total_pending_transcations = len(transcations.filter(status='pending'))
    total_rejected_transcations = len(transcations.filter(status='rejected'))
    total_revenue = sum(transcations.filter(status='approved').values_list('amount', flat=True))
    return render(request, 'support/reports.html', {'transcations': transcations, 'total_transcations': total_transcations, 'total_approved_transcations': total_approved_transcations, 'total_pending_transcations': total_pending_transcations, 'total_rejected_transcations': total_rejected_transcations})

def settings(request):
    return render(request, 'support/settings.html')
    

def users(request):
    users = TelegramUser.objects.all()
    return render(request, 'support/users.html', {'users': users})
    