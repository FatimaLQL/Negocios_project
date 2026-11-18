from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Giro, Negocio, Rol, Usuario

@admin.register(Giro)
class GiroAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    
admin.site.register(Rol)
admin.site.register(Negocio)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
        ('Negocio y rol', {'fields': ('negocio', 'rol')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos del sistema', {'fields': ('email', 'negocio', 'rol')}),
    )
    list_display = ('username', 'email', 'negocio', 'rol', 'is_active')