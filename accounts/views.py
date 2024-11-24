# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from accounts.models import TelegramUser
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
                "message": "Registration successful."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class FilterUsersByPhoneView(generics.ListAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username', None)
        if username:
            users = TelegramUser.objects.filter(username=username)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Phone number not provided."}, status=status.HTTP_400_BAD_REQUEST)