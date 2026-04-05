from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    """
    list_display = ['username', 'email', 'full_name', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'full_name']
    ordering = ['-created_at']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('full_name',)}),
    )
