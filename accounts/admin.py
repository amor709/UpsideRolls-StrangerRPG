from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
        'date_joined',
        'last_login',
    )
    ordering = ('username',)
    list_per_page = 10

    fieldsets = (
        ("Información personal", {
            'fields': ('username', 'email', 'password')
        }),
        ("Permisos", {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ("Fechas importantes", {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        ("Crear nuevo usuario", {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )