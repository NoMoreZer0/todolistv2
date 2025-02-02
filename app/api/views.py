from django.http import HttpResponse
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

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


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return core_models.Task.objects.filter(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return core_models.User.objects.filter(pk=self.request.user.id)


class PushTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.PushTokenCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.PushTokenCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({})


class PingView(APIView):
    def get(self, request):
        return Response({"message": "pong"})


def status(request):
    get_user_model().objects.exists()
    return HttpResponse("")
