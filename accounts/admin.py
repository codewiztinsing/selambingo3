from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserAdmin(UserAdmin):
    list_display = ('username', 'telegram_id', 'telegram_username', 'phone', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_bot')
    search_fields = ('username', 'telegram_id', 'telegram_username', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Telegram Info'), {'fields': ('telegram_id', 'telegram_username', 'first_name', 'last_name', 'language_code', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'telegram_id', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


