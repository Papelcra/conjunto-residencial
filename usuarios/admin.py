from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'username', 'get_full_name', 'rol', 'documento', 'telefono',
        'is_staff', 'is_active', 'date_joined'
    )
    list_filter = ('rol', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'documento', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email', 'documento', 'telefono')
        }),
        ('Rol y permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name', 'last_name',
                'email', 'documento', 'telefono', 'rol', 'is_staff', 'is_active'
            ),
        }),
    )