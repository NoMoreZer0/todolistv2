from rest_framework.authtoken.models import Token
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


class AuthenticationService:
    def __init__(self, user):
        self.user = user

    def authenticate_token(self):
        Token.objects.filter(user=self.user).delete()
        token = Token.objects.create(user=self.user)
        return token.key


class FCMService:
    def __init__(self, user):
        self.user = user

    def send_message(self, title, message):
        device = FCMDevice.objects.get(user=self.user)
        fcm_message = Message(notification=Notification(title=title, body=message))
        device.send_message(fcm_message)
