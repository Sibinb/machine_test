from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response

from general.helpers import get_refresh_tokens_for_user

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            # sending jwt token
            tokens = get_refresh_tokens_for_user(user)
            response_data = {"status": "Success", "tokens": tokens}
            return Response({"app_data": response_data, "StatusCode": 6000})
        else:
            response_data = {"status": "Failed",
                "message": "Invalid credentials"}
            return Response({"app_data": response_data, "StatusCode": 6001})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            response_data = {"message": "Username already in use"}
            return Response({"app_data": response_data, "StatusCode": 6001})
        else:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            if user:
                response_data = {"message": "Registration successful"}
                return Response({"app_data": response_data, "StatusCode": 6000})
            else:
                response_data = {"message": "Failed to register user"}
                return Response({"app_data": response_data, "StatusCode": 6001})

