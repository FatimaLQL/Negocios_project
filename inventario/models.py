from django.db import models
from django.conf import settings



class Categoria(models.Model):
    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=80)

    class Meta:
        db_table = 'categorias'
        constraints = [
            models.UniqueConstraint(
                fields=['negocio', 'nombre'], name='categoria_unica_por_negocio'
            ),
        ]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    codigo = models.CharField(max_length=50, null=True, blank=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    unidad_venta = models.CharField(max_length=20, default='Unidad')
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    existencias = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    proveedores = models.ManyToManyField(
        'contactos.Proveedor', blank=True, db_table='productos_proveedores'
    )

    class Meta:
        db_table = 'productos'
        constraints = [
            models.UniqueConstraint(
                fields=['negocio', 'codigo'], name='producto_codigo_unico_por_negocio'
            ),
            models.CheckConstraint(
                condition=models.Q(precio_venta__gte=0), name='producto_precio_no_negativo'
            ),
            models.CheckConstraint(
                condition=models.Q(costo__isnull=True) | models.Q(costo__gte=0),
                name='producto_costo_no_negativo',
            ),
            models.CheckConstraint(
                condition=models.Q(existencias__gte=0), name='producto_existencias_no_negativas'
            ),
        ]

        

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.CharField(max_length=255, blank=True)
    disponible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'servicios'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0), name='servicio_precio_no_negativo'
            ),
        ]

    def __str__(self):
        return self.nombre


class MovimientoInventario(models.Model):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    TIPOS = [(ENTRADA, 'Entrada'), (SALIDA, 'Salida')]

    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'movimientos_inventario'
        verbose_name_plural = 'movimientos de inventario'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0), name='movimiento_cantidad_positiva'
            ),
            models.CheckConstraint(
                condition=models.Q(tipo__in=['entrada', 'salida']),
                name='movimiento_tipo_valido',
            ),
        ]

    def __str__(self):
        return f'{self.tipo} de {self.cantidad} - {self.producto}'


    
    