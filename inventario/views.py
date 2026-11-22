from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal, InvalidOperation

from .models import Producto, Categoria


@login_required
def crear_producto(request):
    if request.method != 'POST':
        return redirect('productos')

    negocio = request.user.negocio

    codigo = request.POST.get('codigo', '').strip() or None
    nombre = request.POST.get('nombre', '').strip()
    categoria_id = request.POST.get('categoria', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()
    unidad_venta = request.POST.get('unidad_venta', 'Unidad').strip()
    precio_venta = request.POST.get('precio_venta', '').strip()
    costo = request.POST.get('costo', '').strip()
    existencias = request.POST.get('existencias', '0').strip()
    stock_minimo = request.POST.get('stock_minimo', '0').strip()

    if not nombre or not precio_venta:
        messages.error(request, 'El nombre y el precio de venta son obligatorios.')
        return redirect('productos')

    try:
        precio = Decimal(precio_venta)
        costo_valor = Decimal(costo) if costo else None
        existencias_valor = Decimal(existencias or '0')
        stock_minimo_valor = Decimal(stock_minimo or '0')

        if not all(valor.is_finite() for valor in [
            precio,
            existencias_valor,
            stock_minimo_valor,
            *([costo_valor] if costo_valor is not None else [])
        ]):
            raise InvalidOperation

        if precio < 0 or (costo_valor is not None and costo_valor < 0):
            raise InvalidOperation

        if existencias_valor < 0 or stock_minimo_valor < 0:
            raise InvalidOperation

    except (InvalidOperation, ValueError):
        messages.error(request, 'Verifica que los precios y cantidades sean números válidos y no negativos.')
        return redirect('productos')

    categoria = None

    if categoria_id:
        try:
            categoria = Categoria.objects.get(
                pk=categoria_id,
                negocio=negocio
            )
        except Categoria.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no es válida.')
            return redirect('productos')

    try:
        with transaction.atomic():
            Producto.objects.create(
                negocio=negocio,
                categoria=categoria,
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion or None,
                unidad_venta=unidad_venta or 'Unidad',
                precio_venta=precio,
                costo=costo_valor,
                existencias=existencias_valor,
                stock_minimo=stock_minimo_valor,
                activo=True
            )

        messages.success(request, 'Producto registrado correctamente.')

    except IntegrityError:
        messages.error(request, 'El código ya está registrado en tu negocio.')

    return redirect('productos')

@login_required
def editar_producto(request, producto_id):
    negocio = request.user.negocio

    try:
        producto = Producto.objects.get(
            pk=producto_id,
            negocio=negocio
        )
    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe.')
        return redirect('productos')

    if request.method != 'POST':
        return redirect('productos')

    codigo = request.POST.get('codigo', '').strip() or None
    nombre = request.POST.get('nombre', '').strip()
    categoria_id = request.POST.get('categoria', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()
    unidad_venta = request.POST.get('unidad_venta', 'Unidad').strip()

    try:
        precio = Decimal(request.POST.get('precio_venta', '').strip())
        costo_texto = request.POST.get('costo', '').strip()
        costo_valor = Decimal(costo_texto) if costo_texto else None

        existencias_valor = Decimal(
            request.POST.get('existencias', '0').strip() or '0'
        )
        stock_minimo_valor = Decimal(
            request.POST.get('stock_minimo', '0').strip() or '0'
        )

        valores = [precio, existencias_valor, stock_minimo_valor]
        if costo_valor is not None:
            valores.append(costo_valor)

        if not all(v.is_finite() for v in valores):
            raise InvalidOperation

        if not nombre or any(v < 0 for v in valores):
            raise InvalidOperation

        if existencias_valor != existencias_valor.to_integral_value():
            raise InvalidOperation

        if stock_minimo_valor != stock_minimo_valor.to_integral_value():
            raise InvalidOperation

    except (InvalidOperation, ValueError):
        messages.error(request, 'Verifica los datos del producto.')
        return redirect('productos')

    categoria = None

    if categoria_id:
        try:
            categoria = Categoria.objects.get(
                pk=categoria_id,
                negocio=negocio
            )
        except Categoria.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no es válida.')
            return redirect('productos')

    try:
        with transaction.atomic():
            producto.codigo = codigo
            producto.nombre = nombre
            producto.categoria = categoria
            producto.descripcion = descripcion or None
            producto.unidad_venta = unidad_venta or 'Unidad'
            producto.precio_venta = precio
            producto.costo = costo_valor
            producto.existencias = existencias_valor
            producto.stock_minimo = stock_minimo_valor
            producto.save()

        messages.success(request, 'Producto actualizado correctamente.')

    except IntegrityError:
        messages.error(request, 'El código ya está registrado en tu negocio.')

    return redirect('productos')

@login_required
def desactivar_producto(request, producto_id):
    if request.method != 'POST':
        return redirect('productos')

    try:
        producto = Producto.objects.get(
            pk=producto_id,
            negocio=request.user.negocio,
            activo=True
        )

        producto.activo = False
        producto.save(update_fields=['activo'])

        messages.success(
            request,
            'Producto desactivado correctamente.'
        )

    except Producto.DoesNotExist:
        messages.error(request, 'El producto no existe o ya está desactivado.')

    return redirect('productos')

@login_required
def reactivar_producto(request, producto_id):
    if request.method != 'POST':
        return redirect('productos')

    try:
        producto = Producto.objects.get(
            pk=producto_id,
            negocio=request.user.negocio,
            activo=False
        )

        producto.activo = True
        producto.save(update_fields=['activo'])

        messages.success(
            request,
            'Producto reactivado correctamente.'
        )

    except Producto.DoesNotExist:
        messages.error(
            request,
            'El producto no existe o ya está activo.'
        )

    return redirect('productos')