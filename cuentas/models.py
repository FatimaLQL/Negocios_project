from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Giro(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = 'giros'
        verbose_name = 'Tipo de negocio'
        

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField (max_length=40, unique=True)

    class Meta:
        db_table = 'roles'
        verbose_name_plural = 'roles'

    def __str__(self):
        return self.nombre

class Negocio(models.Model):
    nombre = models.CharField(max_length=120)
    giro = models.ForeignKey(Giro, on_delete=models.PROTECT, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField (default=True)
    creado_en = models.DateTimeField(auto_now_add=TimeoutError)


    class Meta:
        db_table = 'negocios'

        def __str__(self):
            return self.nombre

class Usuario(AbstractUser):
    email = models.EmailField('Correo electronico', unique=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.PROTECT, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)

    class Meta: 
        db_table = 'Usuarios'