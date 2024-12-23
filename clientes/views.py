from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from utils.email_service import EmailService
from .forms import SignUpForm, VerificarCorreoForm, UpdateProfileForm, LoginForm
from .models import InformacionCliente


def signup_view(request):
    if request.user.is_authenticated:
        messages.error(request, "Ya estás autenticado/a.")
        return redirect("clientes:profile")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            messages.success(
                request,
                "Cuenta creada con éxito. Por favor, verifica tu correo electrónico.",
            )
            return redirect("clientes:profile")
        else:
            messages.error(
                request,
                "Hubo errores en el formulario. Por favor, corrígelos e intenta nuevamente.",
            )
    else:
        form = SignUpForm()

    return render(request, "clientes/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, "Ya estás autenticado/a.")
        return redirect("clientes:profile")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Bienvenido/a, {user.username}!")
            return redirect("main:home")
        else:
            messages.error(request, form.error_messages)

    else:
        form = LoginForm()

    return render(request, "clientes/login.html", {"form": form})


@login_required
def logout_view(request):
    messages.success(request, "¡Hasta luego!")
    logout(request)
    return redirect("main:home")


@login_required
def profile_view(request):
    cliente_info = get_object_or_404(InformacionCliente, cliente=request.user)

    # Inicialización de formularios
    form = UpdateProfileForm(instance=cliente_info)
    verificar_correo_form = VerificarCorreoForm()  # Inicializa siempre este formulario

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=cliente_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Información del cliente actualizada con éxito.")
            return redirect("clientes:profile")

    return render(
        request,
        "clientes/profile.html",
        {
            "cliente_info": cliente_info,
            "update_form": form,
            "verificar_correo_form": verificar_correo_form,
        },
    )
@login_required
def verificar_correo(request):
    if request.method == "POST":
        form = VerificarCorreoForm(request.POST, user=request.user)  # Pasa el usuario al formulario
        if form.is_valid():
            try:
                perfil = get_object_or_404(InformacionCliente, cliente=request.user)
                perfil.verificado = True
                perfil.save()
                return JsonResponse({"success": True, "message": "Correo electrónico verificado con éxito."})
            except InformacionCliente.DoesNotExist:
                return JsonResponse({"success": False, "message": "No se encontró información del cliente."})
        else:
            # Agregar manejo de errores de formulario
            return JsonResponse({"success": False, "message": "Formulario inválido."})
    return JsonResponse({"success": False, "message": "Método no permitido."})

@login_required
def reenvio_correo_validacion(request):
    try:
        perfil_usuario = get_object_or_404(InformacionCliente, cliente=request.user)

        perfil_usuario.generar_codigo_verificacion()
        perfil_usuario.save()

        EmailService.enviar_codigo_verificacion(perfil=perfil_usuario)

        return JsonResponse(
            {"success": True, "message": "Correo de validación enviado nuevamente."}
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
