from django.contrib import admin

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'negocio')
    list_filter = ('negocio',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'codigo', 'categoria', 'precio_venta',
        'existencias', 'stock_minimo', 'activo', 'negocio',
    )
    search_fields = ('nombre', 'codigo')
    list_filter = ('negocio', 'categoria', 'activo')
    filter_horizontal = ('proveedores',)