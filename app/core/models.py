from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from app.core.managers import UserManager


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Время последнего изменения",
        db_index=True,
    )


class Task(TimeStampMixin):
    title = models.CharField()
    description = models.TextField()
    schedule = models.DateTimeField(blank=True, null=True)


class User(AbstractBaseUser, TimeStampMixin, PermissionsMixin):
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    objects = UserManager()
    email = models.EmailField(unique=True)
    name = models.CharField(null=True, blank=True)
    USERNAME_FIELD = "email"
    is_staff = models.BooleanField(
        default=False, verbose_name="Доступ в админ панель"
    )
    is_active = models.BooleanField(default=True)

    def json(self):
        return {
            "name": self.name,
            "email": self.email
        }

    def __str__(self) -> str:
        return f"{self.email}"


