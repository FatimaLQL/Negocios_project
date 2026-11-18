from django.db import models


class Cliente(models.Model):
    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(max_length=120, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clientes'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'.strip()


class Proveedor(models.Model):
    negocio = models.ForeignKey('cuentas.Negocio', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=120)
    contacto = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(max_length=120, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'proveedores'
        verbose_name_plural = 'proveedores'

    def __str__(self):
        return self.nombre