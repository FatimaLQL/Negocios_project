from django.contrib import admin
from django.db import models
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventario.models import Producto, Categoria
from contactos.models import Cliente
from contactos.views import clientes as clientes_view
from ventas.models import Venta
from django.utils import timezone
from inventario.views import (crear_producto, editar_producto, desactivar_producto, reactivar_producto)


@login_required
def inicio(request):
    usuario = request.user

    negocio = usuario.negocio
    hoy = timezone.localdate()

    ventas_hoy = Venta.objects.filter(
        negocio=negocio,
        estado='completada',
        fecha__date=hoy
    ).aggregate(
        total=models.Sum('total')
    )['total'] or 0

    productos_registrados = Producto.objects.filter(
        negocio=negocio,
        activo=True
    ).count()

    clientes_registrados = Cliente.objects.filter(
        negocio=negocio
    ).count()

    productos_stock_bajo = Producto.objects.filter(
        negocio=negocio,
        activo=True,
        existencias__lte=models.F('stock_minimo')
    ).order_by('existencias')

    ventas_recientes = Venta.objects.filter(
        negocio=negocio
    ).select_related('cliente').order_by('-fecha')[:5]

    return render(request, 'dashboard.html', {
        'active': 'inicio',
        'negocio': negocio,
        'administrador': f"{usuario.first_name} {usuario.last_name}".strip() or usuario.correo,
        'correo': usuario.correo,
        'giro': negocio.giro,
        'ventas_hoy': ventas_hoy,
        'productos_registrados': productos_registrados,
        'clientes_registrados': clientes_registrados,
        'productos_stock_bajo': productos_stock_bajo,
        'ventas_recientes': ventas_recientes,
    })


def ventas(request):
    return render(request, 'ventas.html', {
        'active': 'ventas'
    })

@login_required
def productos(request):
    negocio = request.user.negocio

    productos = Producto.objects.filter(
        negocio=negocio,
        activo=True
    ).select_related('categoria').order_by('nombre')

    total_productos = Producto.objects.filter(
        negocio=negocio
    ).count()

    productos_activos = Producto.objects.filter(
        negocio=negocio,
        activo=True
    ).count()

    productos_desactivados = Producto.objects.filter(
        negocio=negocio,
        activo=False
    ).count()

    productos_stock_bajo = Producto.objects.filter(
        negocio=negocio,
        activo=True,
        existencias__lte=models.F('stock_minimo')
    ).count()

    categorias = Categoria.objects.filter(
        negocio=negocio
    ).order_by('nombre')

    return render(request, 'productos.html', {
        'active': 'productos',
        'productos': productos,
        'categorias': categorias,
        'total_productos': total_productos,
        'productos_activos': productos_activos,
        'productos_desactivados': productos_desactivados,
        'productos_stock_bajo': productos_stock_bajo
    })

@login_required
def productos_desactivados(request):
    negocio = request.user.negocio

    productos = Producto.objects.filter(
        negocio=negocio,
        activo=False
    ).select_related('categoria').order_by('nombre')

    return render(request, 'productos_desactivados.html', {
        'active': 'productos',
        'productos': productos
    })

def inventario(request):
    return render(request, 'inventario.html', {
        'active': 'inventario'
    })




def proveedores(request):
    return render(request, 'proveedores.html', {
        'active': 'proveedores'
    })


def servicios(request):
    return render(request, 'servicios.html', {
        'active': 'servicios'
    })


def cotizaciones(request):
    return render(request, 'cotizaciones.html', {
        'active': 'cotizaciones'
    })


def reportes(request):
    return render(request, 'reportes.html', {
        'active': 'reportes'
    })


def usuarios(request):
    return render(request, 'usuarios.html', {
        'active': 'usuarios'
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('cuentas.urls')),
    path('ventas/', include('ventas.urls')),

    path('', inicio, name='inicio'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>', editar_producto, name='editar_producto'),
    path('productos/desactivar/<int:producto_id>/', desactivar_producto, name='desactivar_producto'),
    path('productos/reactivar/<int:producto_id>/', reactivar_producto, name='reactivar_producto'),
    path('productos/desactivados/', productos_desactivados, name='productos_desactivados'),
    path('productos/', productos, name='productos'),
    path('inventario/', inventario, name='inventario'),
    path('clientes/', clientes_view, name='clientes'),
    path('proveedores/', proveedores, name='proveedores'),
    path('servicios/', servicios, name='servicios'),
    path('cotizaciones/', cotizaciones, name='cotizaciones'),
    path('reportes/', reportes, name='reportes'),
    path('usuarios/', usuarios, name='usuarios'),
]
