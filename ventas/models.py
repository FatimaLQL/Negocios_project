from django.db import models
from django.conf import settings

# Create your models here.

class MetodoPago(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'metodos_pago'
        managed = False

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    id = models.AutoField(primary_key=True)

    negocio = models.ForeignKey(
        'cuentas.Negocio',
        on_delete=models.DO_NOTHING,
        db_column='negocio_id'
    )

    folio = models.IntegerField()

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        db_column='usuario_id'
    )

    cliente = models.ForeignKey(
        'contactos.Cliente',
        on_delete=models.DO_NOTHING,
        db_column='cliente_id',
        null=True,
        blank=True
    )

    cotizacion_id = models.IntegerField(
        null=True,
        blank=True
    )

    metodo_pago = models.ForeignKey(
        MetodoPago,
        on_delete=models.DO_NOTHING,
        db_column='metodo_pago_id'
    )

    fecha = models.DateTimeField()

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    monto_recibido = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    cambio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=12,
        default='completada'
    )

    class Meta:
        db_table = 'ventas'
        managed = False

    def __str__(self):
        return f"Venta #{self.folio}"


class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column='venta_id'
    )

    producto = models.ForeignKey(
        'inventario.Producto',
        on_delete=models.DO_NOTHING,
        db_column='producto_id',
        null=True,
        blank=True
    )

    servicio_id = models.IntegerField(
        null=True,
        blank=True
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = 'detalle_venta'
        managed = False

    def __str__(self):
        return f"Detalle de venta #{self.venta_id}"