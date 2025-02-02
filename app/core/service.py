from rest_framework.authtoken.models import Token


class AuthenticationService:
    def __init__(self, user):
        self.user = user

    def authenticate_token(self):
        Token.objects.filter(user=self.user).delete()
        token = Token.objects.create(user=self.user)
        return token.key
