from django.conf import settings
from django.db import models


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = 'metodos_pago'
        verbose_name = 'método de pago'
        verbose_name_plural = 'métodos de pago'

    def __str__(self):
        return self.nombre


class Cotizacion(models.Model):
    PENDIENTE = 'pendiente'
    ACEPTADA = 'aceptada'
    RECHAZADA = 'rechazada'
    CONVERTIDA = 'convertida'
    ESTADOS = [
        (PENDIENTE, 'Pendiente'),
        (ACEPTADA, 'Aceptada'),
        (RECHAZADA, 'Rechazada'),
        (CONVERTIDA, 'Convertida'),
    ]

    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    cliente = models.ForeignKey(
        'contactos.Cliente', on_delete=models.PROTECT, null=True, blank=True
    )
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=12, choices=ESTADOS, default=PENDIENTE)

    class Meta:
        db_table = 'cotizaciones'
        verbose_name = 'cotización'
        verbose_name_plural = 'cotizaciones'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total__gte=0), name='cotizacion_total_no_negativo'
            ),
            models.CheckConstraint(
                condition=models.Q(
                    estado__in=['pendiente', 'aceptada', 'rechazada', 'convertida']
                ),
                name='cotizacion_estado_valido',
            ),
        ]

    def __str__(self):
        return f'Cotización {self.pk}'


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(
        Cotizacion, on_delete=models.CASCADE, related_name='detalles'
    )
    producto = models.ForeignKey(
        'inventario.Producto', on_delete=models.PROTECT, null=True, blank=True
    )
    servicio = models.ForeignKey(
        'inventario.Servicio', on_delete=models.PROTECT, null=True, blank=True
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_cotizacion'
        verbose_name = 'detalle de cotización'
        verbose_name_plural = 'detalles de cotización'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0), name='detcot_cantidad_positiva'
            ),
            models.CheckConstraint(
                condition=models.Q(precio_unitario__gte=0), name='detcot_precio_no_negativo'
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(producto__isnull=False, servicio__isnull=True)
                    | models.Q(producto__isnull=True, servicio__isnull=False)
                ),
                name='detcot_producto_o_servicio',
            ),
        ]

    def __str__(self):
        return f'Renglón de la cotización {self.cotizacion_id}'


class Venta(models.Model):
    COMPLETADA = 'completada'
    CANCELADA = 'cancelada'
    ESTADOS = [(COMPLETADA, 'Completada'), (CANCELADA, 'Cancelada')]

    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    folio = models.PositiveIntegerField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    cliente = models.ForeignKey(
        'contactos.Cliente', on_delete=models.PROTECT, null=True, blank=True
    )
    cotizacion = models.ForeignKey(
        Cotizacion, on_delete=models.PROTECT, null=True, blank=True
    )
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    monto_recibido = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    cambio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default=COMPLETADA)

    class Meta:
        db_table = 'ventas'
        constraints = [
            models.UniqueConstraint(
                fields=['negocio', 'folio'], name='venta_folio_unico_por_negocio'
            ),
            models.CheckConstraint(
                condition=models.Q(total__gte=0), name='venta_total_no_negativo'
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=['completada', 'cancelada']),
                name='venta_estado_valido',
            ),
        ]

    def __str__(self):
        return f'Venta {self.folio}'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(
        'inventario.Producto', on_delete=models.PROTECT, null=True, blank=True
    )
    servicio = models.ForeignKey(
        'inventario.Servicio', on_delete=models.PROTECT, null=True, blank=True
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'detalle de venta'
        verbose_name_plural = 'detalles de venta'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0), name='detventa_cantidad_positiva'
            ),
            models.CheckConstraint(
                condition=models.Q(precio_unitario__gte=0), name='detventa_precio_no_negativo'
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(producto__isnull=False, servicio__isnull=True)
                    | models.Q(producto__isnull=True, servicio__isnull=False)
                ),
                name='detventa_producto_o_servicio',
            ),
        ]

    def __str__(self):
        return f'Renglón de la venta {self.venta_id}'