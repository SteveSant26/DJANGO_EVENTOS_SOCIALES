from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from utils.email_service import EmailService

from .forms import VerificarCorreoForm, UpdateProfileForm
from .models import InformacionCliente



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
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        user = request.user
        info_cliente = InformacionCliente.objects.get(cliente=user)

        if info_cliente.verificado:
            messages.warning(request, "Ya te has validado")
            return redirect("clientes:profile")

        form = VerificarCorreoForm(request.POST, user=user) 
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"success": True, "message": "Correo electrónico verificado con éxito."}
            )
        else:
            messages.warning(request, form.errors)
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
