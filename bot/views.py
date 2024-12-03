from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import WalletSerializer



def check_balance_view(request):
    pass
    



def transfer(request):
    sender = request.GET.get("sender",None)
    receiver = request.GET.get("receiver",None)

    


class WalletBalanceView(APIView):
    """
    View to create a balance for a user's wallet.
    """
    def post(self, request):
        """
        Create a new balance for the user's wallet.
        """
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            wallet, created = Wallet.objects.get_or_create(
                user=request.user,
                defaults={
                    'balance': serializer.validated_data['balance']
                }
            )
            if not created:
                wallet.balance = serializer.validated_data['balance']
                wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)