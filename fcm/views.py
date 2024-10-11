from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import *
from django.contrib.auth import get_user_model
from .fcm_service import send_fcm_notification
from rest_framework.permissions import AllowAny
from .models import FCMToken

User = get_user_model()



class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # This is now a user object
            Token.objects.filter(user=user).delete()  # Delete old tokens
            token, created = Token.objects.get_or_create(user=user)

            # Now we can save the fcm_token in the FCMToken table
            fcm_token = request.data.get('fcm_token')
            if fcm_token:
                # Create or update FCMToken for the user
                FCMToken.objects.create(user=user, fcm_token=fcm_token)

            return Response({
                'auth_token': token.key,
                'user_id': user.id,
                'fcm_token': fcm_token  # Return the stored fcm_token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendNotificationView(APIView):
    def post(self, request):
        auth_token = request.headers.get('Authorization')
        user = Token.objects.get(key=auth_token.split(' ')[1]).user
        fcm_token = request.data.get('fcm_token')
        title = request.data.get('title')
        message = request.data.get('message')
        
        if user.fcm_token == fcm_token:
            response = send_fcm_notification(fcm_token, title, message)
            return Response({"message": "Notification sent successfully", "fcm_response": response}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid FCM token"}, status=status.HTTP_400_BAD_REQUEST)
