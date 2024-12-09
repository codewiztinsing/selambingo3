# from django.shortcuts import render
# from django.http import JsonResponse
# from accounts.models import TelegramUser
# from .models import Wallet
# # Create your views here.


# def pay_with_chapa(request):
#     context = {}
#     return render(request,"payments/index.html",context)

# def get_balance(request):
#     username = request.GET.get('username')
#     balance = Wallet.objects.filter(user__username=username).first().balance
#     return JsonResponse({'balance': balance})