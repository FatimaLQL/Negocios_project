from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Giro, Negocio, Rol, Usuario


@admin.register(Giro)
class GiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'giro', 'telefono', 'activo')
    search_fields = ('nombre', 'telefono')
    list_filter = ('activo', 'giro')


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    ordering = ('correo',)
    list_display = (
        'correo',
        'first_name',
        'last_name',
        'negocio',
        'rol',
        'is_active',
        'is_staff',
    )
    search_fields = ('correo', 'first_name', 'last_name')

    fieldsets = (
        ('Acceso', {
            'fields': ('correo', 'password')
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name')
        }),
        ('Negocio', {
            'fields': ('negocio', 'rol')
        }),
        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Fechas', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        ('Crear usuario', {
            'classes': ('wide',),
            'fields': (
                'correo',
                'first_name',
                'last_name',
                'negocio',
                'rol',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            ),
        }),
    )