from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from negocio.models import Evento, Servicio
from clientes.models import InformacionCliente
from .models import ReservaEvento, ReservaEventoServicio
from .forms import (
    ReservaEventoForm,
    ReservaEventoServicioForm,
    ReservaEventoConfirmForm,
)
from utils.email_service import EmailService


@login_required
def reservas_view(request):
    parametro_busqueda = request.GET.get("query", "")

    reservas = (
        ReservaEvento.objects.all()
        if request.user.is_superuser
        else ReservaEvento.objects.filter(cliente=request.user)
    )

    if parametro_busqueda:
        reservas = reservas.filter(
            Q(evento__nombre__icontains=parametro_busqueda)
            | Q(cliente__username__icontains=parametro_busqueda)
        )

    reservas = reservas.select_related("evento", "cliente").prefetch_related("fotos")

    todas_reservas = [
        {
            "reserva": reserva,
            "imagen_url": (
                reserva.fotos.first().foto.url if reserva.fotos.exists() else None
            ),
        }
        for reserva in reservas
    ]

    return render(request, "reservas/index.html", {"reservas_items": todas_reservas})


@login_required
def reserva_new(request, evento_id):
    cliente_info = get_object_or_404(InformacionCliente, cliente=request.user)
    if not cliente_info.verificado:
        messages.warning(
            request,
            "Debes verificar tu correo antes de poder alquilar un espacio.",
        )
        return redirect("clientes:profile")

    evento = get_object_or_404(Evento, id=evento_id)
    session_key = f"servicios_seleccionados_{evento_id}"

    formEventoReserva = None
    formEventoReservaServicios = None

    if request.method == "POST":
        if "add_service" in request.POST:
            formEventoReservaServicios = ReservaEventoServicioForm(request.POST)
            if formEventoReservaServicios.is_valid():
                servicio = formEventoReservaServicios.cleaned_data["servicio"]
                cantidad = formEventoReservaServicios.cleaned_data["cantidad"]

                if session_key not in request.session:
                    request.session[session_key] = []

                request.session[session_key].append(
                    {"id": servicio.id, "nombre": servicio.nombre, "cantidad": cantidad}
                )
                request.session.modified = True

                messages.success(request, "Servicio añadido correctamente.")
            else:
                messages.error(request, "Error al añadir el servicio.")

            return redirect("reservas:reserva_new", evento_id=evento_id)

        if "delete_service" in request.POST:
            service_id = int(request.POST.get("service_id", -1))
            servicios_seleccionados = request.session.get(session_key, [])
            servicios_seleccionados = [
                s for s in servicios_seleccionados if s["id"] != service_id
            ]
            request.session[session_key] = servicios_seleccionados
            request.session.modified = True
            messages.success(request, "Servicio eliminado correctamente.")
            return redirect("reservas:reserva_new", evento_id=evento_id)

        formEventoReserva = ReservaEventoForm(request.POST)
        if formEventoReserva.is_valid():
            reserva = formEventoReserva.save(commit=False)
            reserva.cliente = request.user
            reserva.evento = evento
            reserva.save()

            EmailService.enviar_codigo_reserva(reserva)

            servicios_seleccionados = request.session.pop(session_key, [])
            for servicio_data in servicios_seleccionados:
                try:
                    servicio = Servicio.objects.get(id=servicio_data["id"])
                    ReservaEventoServicio.objects.create(
                        reserva=reserva,
                        servicio=servicio,
                        cantidad=servicio_data["cantidad"],
                    )
                except Servicio.DoesNotExist:
                    messages.error(
                        request, f"El servicio con ID {servicio_data['id']} no existe."
                    )

            messages.success(request, "Reserva creada con éxito.")
            return redirect("reservas:reserva_detail", id=reserva.id)
        else:
            print(formEventoReserva.errors)
            messages.error(request, "Error al crear la reserva.")
    else:
        formEventoReserva = ReservaEventoForm()
        formEventoReservaServicios = ReservaEventoServicioForm()

    servicios_seleccionados = request.session.get(session_key, [])

    return render(
        request,
        "reservas/reserva_new.html",
        {
            "formNewReserva": formEventoReserva,
            "formEventoReservaServicios": formEventoReservaServicios,
            "servicios_seleccionados": servicios_seleccionados,
        },
    )

@login_required
def reserva_detail(request, id):
    reserva = get_object_or_404(ReservaEvento, id=id)

    if request.method == "GET":
        fotos = reserva.fotos.all()
        servicios_seleccionados = reserva.reservas_servicios.all()
        formValidateReserva = ReservaEventoConfirmForm()
        return render(
            request,
            "reservas/reserva_detail.html",
            {
                "reserva": reserva,
                "fotos": fotos,
                "servicios_seleccionados": servicios_seleccionados,
                "formValidateReserva": formValidateReserva,
            },
        )


@login_required
def servicios_reserva(request, id):
    reserva = get_object_or_404(ReservaEvento, id=id)

    if not request.user.is_superuser and reserva.cliente != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        formulario = ReservaEventoServicioForm(request.POST)
        if formulario.is_valid():
            servicio = formulario.save()
            reserva.servicios.add(servicio)
            return redirect("reservas:reserva_detail", id=id)

    else:
        formulario = ReservaEventoServicioForm()

    servicios = reserva.servicios_reserva.all()
    return render(
        request,
        "reservas/servicios_reserva.html",
        {
            "reserva": reserva,
            "servicios": servicios,
            "form": formulario,
        },
    )


@login_required
def enviar_correo_reserva(request, id):
    reserva = get_object_or_404(ReservaEvento, id=id)
    EmailService.enviar_codigo_reserva(reserva)
    return JsonResponse({"success": True, "message": "Correo enviado correctamente."})


@login_required
def confirmar_reserva(request, id):
    reserva = get_object_or_404(ReservaEvento, id=id)

    if request.method == "POST":
        formulario = ReservaEventoConfirmForm(request.POST, reserva=reserva)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse(
                {"success": True, "message": "Reserva confirmada correctamente."}
            )
        else:
            return JsonResponse({"success": False, "errors": formulario.errors})

    else:
        formulario = ReservaEventoConfirmForm(reserva=reserva)

    return render(
        request,
        "reservas/reserva_confirm.html",
        {"formulario": formulario, "reserva": reserva},
    )
