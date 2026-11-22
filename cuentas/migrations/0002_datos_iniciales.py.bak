from django.db import migrations

GIROS = [
    'Abarrotes', 'Ropa o zapatos', 'Restaurante', 'Tienda de objetos', 'Farmacia',
    'Ferretería', 'Electrónica', 'Cafetería', 'Auto partes', 'Papelería', 'Joyería',
    'Belleza y cosméticos', 'Panadería', 'Taller mecánico', 'Mercería', 'Limpieza',
    'Carnicería, pescadería o verdulería', 'Veterinaria o tienda para mascotas',
    'Óptica', 'Librería', 'Otros',
]
ROLES = ['Administrador', 'Cajero']


def cargar_datos(apps, schema_editor):
    Giro = apps.get_model('cuentas', 'Giro')
    Rol = apps.get_model('cuentas', 'Rol')
    for nombre in GIROS:
        Giro.objects.get_or_create(nombre=nombre)
    for nombre in ROLES:
        Rol.objects.get_or_create(nombre=nombre)


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_datos, migrations.RunPython.noop),
    ]