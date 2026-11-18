from django.contrib import admin

from .models import Cliente, Proveedor


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'correo', 'negocio')
    search_fields = ('nombre', 'apellido', 'telefono', 'correo')
    list_filter = ('negocio',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'negocio', 'activo')
    search_fields = ('nombre', 'contacto')
    list_filter = ('negocio', 'activo')