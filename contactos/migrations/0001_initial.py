import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cuentas', '0002_datos_iniciales'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Cliente',
                    fields=[
                        ('id', models.AutoField(
                            primary_key=True,
                            serialize=False,
                        )),
                        ('nombre', models.CharField(max_length=80)),
                        ('apellido', models.CharField(
                            blank=True, max_length=80, null=True
                        )),
                        ('telefono', models.CharField(
                            blank=True, max_length=20, null=True
                        )),
                        ('correo', models.EmailField(
                            blank=True, max_length=120, null=True
                        )),
                        ('direccion', models.CharField(
                            blank=True, max_length=200, null=True
                        )),
                        ('creado_en', models.DateTimeField(auto_now_add=True)),
                        ('negocio', models.ForeignKey(
                            db_column='negocio_id',
                            on_delete=django.db.models.deletion.PROTECT,
                            to='cuentas.negocio'
                        )),
                    ],
                    options={
                        'db_table': 'clientes',
                    },
                ),
                migrations.CreateModel(
                    name='Proveedor',
                    fields=[
                        ('id', models.AutoField(
                            primary_key=True,
                            serialize=False,
                        )),
                        ('nombre', models.CharField(max_length=120)),
                        ('contacto', models.CharField(
                            blank=True, max_length=120, null=True
                        )),
                        ('telefono', models.CharField(
                            blank=True, max_length=20, null=True
                        )),
                        ('correo', models.EmailField(
                            blank=True, max_length=120, null=True
                        )),
                        ('direccion', models.CharField(
                            blank=True, max_length=200, null=True
                        )),
                        ('activo', models.BooleanField(default=True)),
                        ('creado_en', models.DateTimeField(auto_now_add=True)),
                        ('negocio', models.ForeignKey(
                            db_column='negocio_id',
                            on_delete=django.db.models.deletion.PROTECT,
                            to='cuentas.negocio'
                        )),
                    ],
                    options={
                        'db_table': 'proveedores',
                        'verbose_name_plural':
                        'proveedores',
                    },
                ),
            ],
        ),
    ]