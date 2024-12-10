from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



def check_balance_view(request):
    pass
    



def transfer(request):
    sender = request.GET.get("sender",None)
    receiver = request.GET.get("receiver",None)

    
