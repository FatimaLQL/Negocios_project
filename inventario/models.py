from django.db import models


class Categoria(models.Model):
    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=80)

    class Meta:
        db_table = 'categorias'
        constraints = [
            models.UniqueConstraint(
                fields=['negocio', 'nombre'], name='categorias_negocio_id_nombre_key'
            ),
        ]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    codigo = models.CharField(max_length=50, null=True, blank=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    unidad_venta = models.CharField(max_length=20, default='Unidad')
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    existencias = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    proveedores = models.ManyToManyField(
        'contactos.Proveedor',
        through='ProductoProveedor',
        through_fields=('producto', 'proveedor'),
        blank=True,
    )

    class Meta:
            db_table = 'productos'
            constraints = [
                models.UniqueConstraint(
                    fields=['negocio', 'codigo'],
                    name='productos_negocio_id_codigo_key'
                ),
                models.CheckConstraint(
                    condition=models.Q(precio_venta__gte=0),
                    name='productos_precio_venta_check'
                ),
                models.CheckConstraint(
                    condition=models.Q(costo__gte=0),
                    name='productos_costo_check'
                ),
                models.CheckConstraint(
                    condition=models.Q(existencias__gte=0),
                    name='productos_existencias_check'
                ),
            ]

    def __str__(self):
        return self.nombre

class ProductoProveedor(models.Model):
    pk = models.CompositePrimaryKey(
        'producto_id',
        'proveedor_id'
    )

    producto = models.ForeignKey(
        'inventario.Producto',
        on_delete=models.CASCADE,
        db_column='producto_id'
    )

    proveedor = models.ForeignKey(
        'contactos.Proveedor',
        on_delete=models.CASCADE,
        db_column='proveedor_id'
    )

    class Meta:
        db_table = 'productos_proveedores'
        managed = False