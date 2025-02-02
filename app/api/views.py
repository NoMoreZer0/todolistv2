from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from app.api import serializers
from app.core import models as core_models


class RegisterUserView(generics.CreateAPIView):
    queryset = core_models.User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.create(serializer.validated_data)
        return Response(response)


class PingView(APIView):
    def get(self, request):
        return Response({"message": "pong"})


def status(request):
    get_user_model().objects.exists()
    return HttpResponse("")
