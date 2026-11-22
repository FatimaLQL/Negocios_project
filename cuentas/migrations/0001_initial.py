import cuentas.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Giro',
                    fields=[
                        ('id', models.AutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name='ID'
                        )),
                        ('nombre', models.CharField(
                            max_length=80,
                            unique=True
                        )),
                    ],
                    options={
                        'verbose_name': 'Tipo de negocio',
                        'db_table': 'giros',
                    },
                ),
                migrations.CreateModel(
                    name='Rol',
                    fields=[
                        ('id', models.AutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name='ID'
                        )),
                        ('nombre', models.CharField(
                            max_length=40,
                            unique=True
                        )),
                    ],
                    options={
                        'verbose_name_plural': 'roles',
                        'db_table': 'roles',
                    },
                ),
                migrations.CreateModel(
                    name='Negocio',
                    fields=[
                        ('id', models.AutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name='ID'
                        )),
                        ('nombre', models.CharField(max_length=120)),
                        ('telefono', models.CharField(
                            blank=True,
                            max_length=20,
                            null=True
                        )),
                        ('activo', models.BooleanField(default=True)),
                        ('creado_en', models.DateTimeField(auto_now_add=True)),
                        ('giro', models.ForeignKey(
                            blank=True,
                            null=True,
                            on_delete=django.db.models.deletion.PROTECT,
                            to='cuentas.giro'
                        )),
                    ],
                    options={
                        'db_table': 'negocios',
                    },
                ),
                migrations.CreateModel(
                    name='Usuario',
                    fields=[
                        ('id', models.AutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name='ID'
                        )),
                        ('password', models.CharField(
                            db_column='contrasena',
                            max_length=255
                        )),
                        ('correo', models.EmailField(
                            db_column='correo',
                            max_length=120,
                            unique=True
                        )),
                        ('first_name', models.CharField(
                            db_column='nombre',
                            max_length=80
                        )),
                        ('last_name', models.CharField(
                            blank=True,
                            db_column='apellido',
                            max_length=80,
                            null=True
                        )),
                        ('is_active', models.BooleanField(
                            db_column='activo',
                            default=True
                        )),
                        ('date_joined', models.DateTimeField(
                            auto_now_add=True,
                            db_column='creado_en'
                        )),
                        ('negocio', models.ForeignKey(
                            db_column='negocio_id',
                            on_delete=django.db.models.deletion.PROTECT,
                            to='cuentas.negocio'
                        )),
                        ('rol', models.ForeignKey(
                            db_column='rol_id',
                            on_delete=django.db.models.deletion.PROTECT,
                            to='cuentas.rol'
                        )),
                    ],
                    options={
                        'db_table': 'usuarios',
                    },
                    managers=[
                        ('objects', cuentas.models.UsuarioManager()),
                    ],
                ),
            ],
        ),
    ]