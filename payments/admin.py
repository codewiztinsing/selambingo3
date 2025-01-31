from django.contrib import admin
from .models import Wallet,Commission,Charge,WinTracker,PaymentSession

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__telegram_username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'balance')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('game_type', 'amount', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('game_type', 'amount')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('game_type', 'amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'player', 'charged', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('game_id', 'player__username')
    readonly_fields = ('created_at', 'updated_at')  

@admin.register(WinTracker)
class WinTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_id', 'win_amount', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'game_id')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'game_id', 'win_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PaymentSession)
class PaymentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'amount', 'created_at', 'updated_at','status')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'session_id')
    readonly_fields = ('created_at', 'updated_at','status')

    fieldsets = (
        (None, {
            'fields': ('user', 'session_id', 'amount','status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )