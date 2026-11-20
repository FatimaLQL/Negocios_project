from django.contrib import admin

from .models import Categoria, Producto, MovimientoInventario,Servicio


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

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible', 'negocio')
    search_fields = ('nombre',)
    list_filter = ('negocio', 'categoria', 'disponible')


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'producto', 'tipo', 'cantidad', 'motivo', 'usuario', 'negocio')
    list_filter = ('negocio', 'tipo')
    search_fields = ('producto__nombre', 'motivo')