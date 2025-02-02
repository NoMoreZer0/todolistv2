from django.urls import path

from app.api.views import RegisterUserView, LoginView, PingView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("ping", PingView.as_view(), name="ping")
]
