import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contactos', '0001_initial'),
        ('cuentas', '0002_datos_iniciales'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Categoria',
                    fields=[
                        ('id', models.AutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name='ID'
                        )),
                        ('nombre', models.CharField(max_length=80)),
                        ('negocio', models.ForeignKey(
                            on_delete=django.db.models.deletion.PROTECT,
                            to='cuentas.negocio'
                        )),
                    ],
                    options={
                        'db_table': 'categorias',
                    },
                ),
                migrations.CreateModel(
                    name='Producto',
                    fields=[
                        ('id', models.AutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name='ID'
                        )),
                        ('codigo', models.CharField(
                            blank=True, max_length=50, null=True
                        )),
                        ('nombre', models.CharField(max_length=150)),
                        ('descripcion', models.TextField(
                            blank=True, null=True
                        )),
                        ('unidad_venta', models.CharField(
                            default='Unidad', max_length=20
                        )),
                        ('precio_venta', models.DecimalField(
                            decimal_places=2, max_digits=10
                        )),
                        ('costo', models.DecimalField(
                            blank=True, decimal_places=2,
                            max_digits=10, null=True
                        )),
                        ('existencias', models.DecimalField(
                            decimal_places=2, default=0, max_digits=10
                        )),
                        ('stock_minimo', models.DecimalField(
                            decimal_places=2, default=0, max_digits=10
                        )),
                        ('activo', models.BooleanField(default=True)),
                        ('creado_en', models.DateTimeField(auto_now_add=True)),
                        ('categoria', models.ForeignKey(
                            blank=True,
                            null=True,
                            on_delete=django.db.models.deletion.PROTECT,
                            to='inventario.categoria'
                        )),
                        ('negocio', models.ForeignKey(
                            on_delete=django.db.models.deletion.PROTECT,
                            to='cuentas.negocio'
                        )),
                        ('proveedores', models.ManyToManyField(
                            blank=True,
                            through='inventario.ProductoProveedor',
                            through_fields=('producto', 'proveedor'),
                            to='contactos.proveedor'
                        )),
                    ],
                    options={
                        'db_table': 'productos',
                    },
                ),
                migrations.CreateModel(
                    name='ProductoProveedor',
                    fields=[
                        ('pk', models.CompositePrimaryKey(
                            'producto_id', 'proveedor_id',
                            serialize=False
                        )),
                        ('producto', models.ForeignKey(
                            db_column='producto_id',
                            on_delete=django.db.models.deletion.CASCADE,
                            to='inventario.producto'
                        )),
                        ('proveedor', models.ForeignKey(
                            db_column='proveedor_id',
                            on_delete=django.db.models.deletion.CASCADE,
                            to='contactos.proveedor'
                        )),
                    ],
                    options={
                        'db_table': 'productos_proveedores',
                        'managed': False,
                    },
                ),
                migrations.AddConstraint(
                    model_name='categoria',
                    constraint=models.UniqueConstraint(
                        fields=('negocio', 'nombre'),
                        name='categorias_negocio_id_nombre_key'
                    ),
                ),
                migrations.AddConstraint(
                    model_name='producto',
                    constraint=models.UniqueConstraint(
                        fields=('negocio', 'codigo'),
                        name='productos_negocio_id_codigo_key'
                    ),
                ),
                migrations.AddConstraint(
                    model_name='producto',
                    constraint=models.CheckConstraint(
                        condition=models.Q(('precio_venta__gte', 0)),
                        name='productos_precio_venta_check'
                    ),
                ),
                migrations.AddConstraint(
                    model_name='producto',
                    constraint=models.CheckConstraint(
                        condition=models.Q(('costo__gte', 0)),
                        name='productos_costo_check'
                    ),
                ),
                migrations.AddConstraint(
                    model_name='producto',
                    constraint=models.CheckConstraint(
                        condition=models.Q(('existencias__gte', 0)),
                        name='productos_existencias_check'
                    ),
                ),
            ],
        ),
    ]