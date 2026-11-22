from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contactos.models import Cliente


@login_required
def clientes(request):
    negocio = request.user.negocio

    if request.method == 'POST':

        accion = request.POST.get('accion')

        # EDITAR CLIENTE
        if accion == 'editar':
            cliente_id = request.POST.get('cliente_id')

            cliente = get_object_or_404(
                Cliente,
                id=cliente_id,
                negocio=negocio
            )

            nombre = request.POST.get('nombre', '').strip()

            if not nombre:
                messages.error(request, 'El nombre del cliente es obligatorio.')
                return redirect('clientes')

            cliente.nombre = nombre
            cliente.apellido = request.POST.get('apellido', '').strip() or None
            cliente.telefono = request.POST.get('telefono', '').strip() or None
            cliente.correo = request.POST.get('correo', '').strip() or None
            cliente.direccion = request.POST.get('direccion', '').strip() or None

            cliente.save()

            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientes')

        # REGISTRAR CLIENTE
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        direccion = request.POST.get('direccion', '').strip()

        if not nombre:
            messages.error(request, 'El nombre del cliente es obligatorio.')
            return redirect('clientes')

        Cliente.objects.create(
            negocio=negocio,
            nombre=nombre,
            apellido=apellido or None,
            telefono=telefono or None,
            correo=correo or None,
            direccion=direccion or None
        )

        messages.success(request, 'Cliente registrado correctamente.')
        return redirect('clientes')

    lista_clientes = Cliente.objects.filter(
        negocio=negocio
    ).order_by('nombre', 'apellido')

    return render(request, 'clientes.html', {
        'active': 'clientes',
        'clientes': lista_clientes,
        'total_clientes': lista_clientes.count(),
    })