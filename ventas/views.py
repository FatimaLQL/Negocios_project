import json

from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max, Sum
from django.utils import timezone

from inventario.models import Producto
from contactos.models import Cliente
from cuentas.models import Negocio
from ventas.models import Venta, DetalleVenta, MetodoPago

@login_required
def ventas_view(request):
    negocio_id = request.user.negocio_id

    if request.method == 'POST':
        try:
            carrito = json.loads(request.POST.get('carrito') or '[]')

            if not isinstance(carrito, list) or not carrito:
                messages.error(request, 'Agrega al menos un producto.')
                return redirect('ventas:ventas')

            metodo_id = request.POST.get('metodo_pago')
            cliente_id = request.POST.get('cliente') or None

            if not metodo_id:
                messages.error(request, 'Selecciona un método de pago.')
                return redirect('ventas:ventas')

            with transaction.atomic():

                # Bloquear el negocio para generar folios consecutivos
                negocio = Negocio.objects.select_for_update().get(
                    pk=negocio_id
                )

                metodo = MetodoPago.objects.get(pk=metodo_id)

                cliente = None
                if cliente_id:
                    cliente = Cliente.objects.get(
                        pk=cliente_id,
                        negocio_id=negocio.pk
                    )

                # Validar y bloquear los productos del carrito
                ids = []
                cantidades = {}

                for item in carrito:
                    producto_id = int(item['id'])
                    cantidad = Decimal(str(item['cantidad']))

                    if producto_id in cantidades:
                        raise ValueError('Hay productos duplicados en el carrito.')

                    if not cantidad.is_finite() or cantidad <= 0:
                        raise ValueError('La cantidad de un producto no es válida.')

                    ids.append(producto_id)
                    cantidades[producto_id] = cantidad

                productos = Producto.objects.select_for_update().filter(
                    id__in=ids,
                    negocio_id=negocio.pk,
                    activo=True
                )

                productos = list(productos)

                if len(productos) != len(ids):
                    raise ValueError('Uno o más productos no están disponibles.')

                total = Decimal('0.00')

                for producto in productos:
                    cantidad = cantidades[producto.id]

                    if cantidad > producto.existencias:
                        raise ValueError(
                            f'Existencias insuficientes para {producto.nombre}.'
                        )

                    total += producto.precio_venta * cantidad

                total = total.quantize(Decimal('0.01'))

                # Validar el cobro
                if metodo.pk == 1:
                    recibido = Decimal(
                        request.POST.get('monto_recibido', '0')
                    )

                    if not recibido.is_finite() or recibido < total:
                        raise ValueError(
                            'El monto recibido no cubre el total de la venta.'
                        )

                    cambio = recibido - total

                else:
                    recibido = None
                    cambio = Decimal('0.00')

                # Generar folio por negocio
                ultimo_folio = Venta.objects.filter(
                    negocio=negocio
                ).aggregate(maximo=Max('folio'))['maximo'] or 0

                folio = ultimo_folio + 1

                # Guardar encabezado de venta
                venta = Venta.objects.create(
                    negocio=negocio,
                    folio=folio,
                    usuario=request.user,
                    cliente=cliente,
                    metodo_pago=metodo,
                    fecha=timezone.now(),
                    total=total,
                    monto_recibido=recibido,
                    cambio=cambio,
                    estado='completada'
                )

                # Guardar detalles y descontar inventario
                for producto in productos:
                    cantidad = cantidades[producto.id]

                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        servicio_id=None,
                        cantidad=cantidad,
                        precio_unitario=producto.precio_venta
                    )

                    producto.existencias -= cantidad
                    producto.save(update_fields=['existencias'])

            messages.success(
                request,
                f'Venta #{folio} registrada correctamente.'
            )

            return redirect('ventas:ventas')

        except (
            ValueError,
            InvalidOperation,
            TypeError,
            KeyError,
            MetodoPago.DoesNotExist,
            Cliente.DoesNotExist,
            Negocio.DoesNotExist
        ) as error:
            messages.error(request, str(error))
            return redirect('ventas:ventas')

    productos = Producto.objects.filter(
        negocio_id=negocio_id,
        activo=True,
        existencias__gt=0
    ).order_by('nombre')

    clientes = Cliente.objects.filter(
        negocio_id=negocio_id
    ).order_by('nombre', 'apellido')

    hoy = timezone.localdate()

    ventas_completadas = Venta.objects.filter(
        negocio_id=negocio_id,
        estado='completada'
    )

    ventas_hoy = ventas_completadas.filter(
        fecha__date=hoy
    ).aggregate(
        total=Sum('total')
    )['total'] or Decimal('0.00')

    total_ventas = ventas_completadas.count()

    productos_vendidos = DetalleVenta.objects.filter(
        venta__negocio_id=negocio_id,
        venta__estado='completada'
    ).aggregate(
        total=Sum('cantidad')
    )['total'] or 0

    return render(request, 'ventas.html', {
        'productos': productos,
        'clientes': clientes,
        'ventas_hoy': ventas_hoy,
        'total_ventas': total_ventas,
        'productos_vendidos': productos_vendidos,
    })