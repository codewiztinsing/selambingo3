# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from accounts.models import TelegramUser
# from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("serializer=   ",serializer)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": {
                    "username": user.username
                },
                "message": "Registration successful."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class FilterUsersByPhoneView(generics.ListAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request, user_id,*args, **kwargs):

        
            try:
                user_id = int(user_id)
                user = TelegramUser.objects.filter(telegram_id=user_id).first()
                if user:
                    serializer = self.get_serializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except TelegramUser.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
       


class AllUsersView(generics.ListAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = TelegramUser.objects.all()

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('login')    
