from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Usuario, Negocio, Giro, Rol


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('password', '')

        usuario = authenticate(
            request,
            correo=correo,
            password=password
        )

        if usuario is not None:
            login(request, usuario)

            destino = request.GET.get('next', 'inicio')

            if not destino.startswith('/') or destino.startswith('//'):
                destino = 'inicio'

            return redirect(destino)

        messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'login.html')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    giros = Giro.objects.order_by('nombre')

    if request.method == 'POST':
        nombre_negocio = request.POST.get('nombre_negocio', '').strip()
        giro_id = request.POST.get('giro', '')
        telefono = request.POST.get('telefono', '').strip()

        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('password', '')
        confirmar_password = request.POST.get('confirmar_password', '')

        if not all([nombre_negocio, giro_id, nombre, correo, password, confirmar_password]):
            messages.error(request, 'Completa todos los campos obligatorios.')

        elif password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')

        elif Usuario.objects.filter(correo__iexact=correo).exists():
            messages.error(request, 'Ya existe una cuenta con ese correo.')

        else:
            try:
                validate_password(password)

                giro = Giro.objects.get(pk=giro_id)
                rol = Rol.objects.get(nombre='Administrador')

                with transaction.atomic():
                    negocio = Negocio.objects.create(
                        nombre=nombre_negocio,
                        giro=giro,
                        telefono=telefono or None
                    )

                    Usuario.objects.create_user(
                        correo=correo,
                        password=password,
                        first_name=nombre,
                        last_name=apellido,
                        negocio=negocio,
                        rol=rol
                    )

                messages.success(
                    request,
                    'Tu negocio y tu cuenta se registraron correctamente. Ya puedes iniciar sesión.'
                )
                return redirect('login')

            except ValidationError as error:
                for mensaje in error.messages:
                    messages.error(request, mensaje)

            except (Giro.DoesNotExist, Rol.DoesNotExist):
                messages.error(
                    request,
                    'No se encontró el giro o el rol de administrador.'
                )

    return render(request, 'registro.html', {'giros': giros})


def logout_view(request):
    logout(request)
    return redirect('login')