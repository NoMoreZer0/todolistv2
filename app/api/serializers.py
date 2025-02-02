from rest_framework import serializers
from django.contrib.auth import authenticate

from app.core import models as core_models
from app.core import service as core_service


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.User
        fields = ['email', 'name', 'password']

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = core_models.User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = core_models.User.objects.get(email=data["email"])
        except core_models.User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid email or password")
        data["user"] = user
        return data

    def create(self, validated_data):
        auth_service = core_service.AuthenticationService(validated_data["user"])
        token = auth_service.authenticate_token()
        return {"token": token}


