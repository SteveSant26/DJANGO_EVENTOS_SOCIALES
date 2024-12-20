from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CrearClienteForm, VerificarCorreoForm, ActualizarClienteForm
from .models import InformacionCliente




def crear_cliente(request):
    if request.method == "POST":
        form = CrearClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cuenta creada con éxito. Por favor, verifica tu correo electrónico.")
            return redirect("verificar_correo")  
    else:
        form = CrearClienteForm()

    return render(request, "clientes/crear_cliente.html", {"form": form})


def verificar_correo(request):
    if request.method == "POST":
        form = VerificarCorreoForm(request.POST)
        if form.is_valid():
            try:
                perfil = InformacionCliente.objects.get(cliente=request.user)
                perfil.verificado = True
                perfil.save()
                messages.success(request, "Correo electrónico verificado con éxito.")
                return redirect("perfil_cliente")  
            except InformacionCliente.DoesNotExist:
                messages.error(request, "No se encontró información del cliente.")
                return redirect("crear_cliente")
    else:
        form = VerificarCorreoForm()

    return render(request, "clientes/verificar_correo.html", {"form": form})


@login_required
def actualizar_cliente(request):
    try:
        cliente_info = InformacionCliente.objects.get(cliente=request.user)
    except InformacionCliente.DoesNotExist:
        messages.error(request, "No se encontraron datos de cliente asociados a tu cuenta.")
        return redirect("crear_cliente")

    if request.method == "POST":
        form = ActualizarClienteForm(request.POST, instance=cliente_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Información del cliente actualizada con éxito.")
            return redirect("perfil_cliente") 
    else:
        form = ActualizarClienteForm(instance=cliente_info)

    return render(request, "clientes/actualizar_cliente.html", {"form": form})
