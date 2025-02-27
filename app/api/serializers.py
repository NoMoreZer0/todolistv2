from rest_framework import serializers
from django.contrib.auth import authenticate

from app.core import models as core_models
from app.core import service as core_service
from fcm_django.models import FCMDevice


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.User
        fields = ["email", "name", "password"]

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = core_models.User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
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


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Task
        fields = ["id", "title", "description", "schedule"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        fcm_service = core_service.FCMService(request.user)
        fcm_service.send_message(title="Congratz!", message="You have created a task!")
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.User
        fields = ["id", "email", "name"]


class PushTokenCreateSerializer(serializers.Serializer):
    token = serializers.CharField()

    def create(self, validated_data):
        FCMDevice.objects.update_or_create(
            registration_id=validated_data["token"],
            defaults={
                "user": self.context["request"].user
            }
        )
