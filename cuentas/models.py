from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UsuarioManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")

        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(correo, password, **extra_fields)


class Giro(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = 'giros'
        verbose_name = 'Tipo de negocio'

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = 'roles'
        verbose_name_plural = 'roles'

    def __str__(self):
        return self.nombre


class Negocio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    giro = models.ForeignKey(
        Giro,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'negocios'

    def __str__(self):
        return self.nombre


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    password = models.CharField(
            max_length=255,
            db_column='contrasena'
        )

    correo = models.EmailField(
        max_length=120,
        unique=True,
        db_column='correo'
    )

    first_name = models.CharField(
        max_length=80,
        db_column='nombre'
    )

    last_name = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        db_column='apellido'
    )

    negocio = models.ForeignKey(
        Negocio,
        on_delete=models.PROTECT,
        db_column='negocio_id'
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        db_column='rol_id'
    )

    is_active = models.BooleanField(
        default=True,
        db_column='activo'
    )

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(
        blank=True,
        null=True
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_column='creado_en'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='usuarios_personalizados',
        db_table='Usuarios_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='usuarios_personalizados',
        db_table='Usuarios_user_permissions'
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['first_name', 'negocio', 'rol']

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.correo