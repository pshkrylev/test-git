from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailConfirmationToken

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_verified', 'subscribed_to_news', 'is_staff')
    list_filter = ('is_verified', 'subscribed_to_news', 'is_staff')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('is_verified', 'subscribed_to_news')}),
    )

@admin.register(EmailConfirmationToken)
class EmailConfirmationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    readonly_fields = ('token', 'created_at')