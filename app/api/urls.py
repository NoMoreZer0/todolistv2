from django.urls import path

from rest_framework import routers

from app.api.views import (
    RegisterUserView,
    LoginView,
    PingView,
    TaskViewSet,
    UserViewSet,
    PushTokenViewSet,
)

router = routers.DefaultRouter()
router.register("task", TaskViewSet, basename="task")
router.register("user", UserViewSet, basename="user")
router.register("push-token", PushTokenViewSet, basename="push_token")

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("ping", PingView.as_view(), name="ping"),
]

urlpatterns += router.urls
