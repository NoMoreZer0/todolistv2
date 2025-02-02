from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)

