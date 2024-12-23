from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CrearClienteForm, VerificarCorreoForm, ActualizarClienteForm, LoginForm
from .models import InformacionCliente




def crear_cliente(request):
    if request.method == "POST":
        form = CrearClienteForm(request.POST)
        if form.is_valid():
            # Crear usuario
            user = form.save()
            login(request, user)
            messages.success(request, "Cuenta creada con éxito. Por favor, verifica tu correo electrónico.")
            return redirect("verificar_correo")  # Ajusta según la lógica de tu proyecto
        else:
            messages.error(request, "Hubo errores en el formulario. Por favor, corrígelos.")
    else:
        form = CrearClienteForm()

    return render(request, "clientes/crear_cliente.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)  # Usa el formulario incorporado de Django
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido/a, {user.username}!")
                return redirect("home")  # Ajusta según tu lógica
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        form = LoginForm()

    return render(request, "clientes/login.html", {"form": form})


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
