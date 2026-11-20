from django.db import migrations

METODOS = ['Efectivo', 'Tarjeta', 'Transferencia']


def cargar(apps, schema_editor):
    MetodoPago = apps.get_model('ventas', 'MetodoPago')
    for nombre in METODOS:
        MetodoPago.objects.get_or_create(nombre=nombre)


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar, migrations.RunPython.noop),
    ]