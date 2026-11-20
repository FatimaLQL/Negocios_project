from django.contrib import admin

from .models import Cotizacion, DetalleCotizacion, DetalleVenta, MetodoPago, Venta

admin.site.register(MetodoPago)


class DetalleCotizacionInline(admin.TabularInline):
    model = DetalleCotizacion
    extra = 1


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'cliente', 'total', 'estado', 'negocio')
    list_filter = ('negocio', 'estado')
    inlines = [DetalleCotizacionInline]


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'folio', 'fecha', 'usuario', 'cliente', 'metodo_pago', 'total', 'estado', 'negocio',
    )
    list_filter = ('negocio', 'estado', 'metodo_pago')
    search_fields = ('folio',)
    inlines = [DetalleVentaInline]