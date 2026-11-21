from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Producto


@login_required
def lista_productos(request):
    productos = Producto.objects.filter(negocio=request.user.negocio)
    return render(request, 'inventario/lista_productos.html', {'productos': productos})