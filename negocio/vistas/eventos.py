from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from ..models import Evento, FotoEvento, TipoEvento, ResenaEvento
from ..forms import ResenaEventoForm
from django.contrib import messages


def listar_eventos(request):
    query = request.GET.get("query", "")
    eventos = Evento.objects.filter(nombre__icontains=query) | Evento.objects.filter(
        descripcion__icontains=query
    )
    datos = [
        {"evento": evento, "foto": FotoEvento.objects.filter(evento=evento).first()}
        for evento in eventos
    ]
    return render(
        request,
        "negocio/eventos/index.html",
        {
            "eventos": datos,
        },
    )


def obtener_evento(request, evento_id):

    evento = get_object_or_404(Evento, pk=evento_id)
    fotos = FotoEvento.objects.filter(evento=evento)
    resenasEvento = ResenaEvento.objects.filter(evento=evento)
    nombreEvento = f"Evento #{evento.id}"

    if request.method == "POST":
        formresena = ResenaEventoForm(request.POST)
        if formresena.is_valid():

            resena = formresena.save(commit=False)
            resena.evento = evento
            resena.autor = request.user
            resena.save()
            messages.success(request, "Reseña creada correctamente.")
            return redirect("negocio:obtener_evento", evento_id)
    formresena = ResenaEventoForm()
    return render(
        request,
        "negocio/eventos/obtener_evento.html",
        {
            "evento": evento,
            "fotos": fotos,
            "nombreEvento": nombreEvento,
            "resenasEvento": resenasEvento,
            "formresena": formresena,
        },
    )


def obtener_dar_calificacion(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    if request.method == "POST":
        form = ResenaEventoForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.evento = evento
            resena.save()

            return render(
                request, "negocio/eventos/obtener_evento.html", {"evento": evento}
            )
    else:
        form = ResenaEventoForm()

    return render(
        request, "negocio/dar_calificacion.html", {"form": form, "evento": evento}
    )


def listar_tipos_eventos(request):
    tipo_eventos = TipoEvento.objects.all()
    return render(
        request, "negocio/eventos/tipo_eventos.html", {"tipo_eventos": tipo_eventos}
    )


def listar_eventos_por_tipo(request, tipo_evento_id):
    tipo_evento = get_object_or_404(TipoEvento, pk=tipo_evento_id)
    query = request.GET.get("query", "")
    eventos = Evento.objects.filter(tipo_evento=tipo_evento).filter(
        nombre__icontains=query
    ) | Evento.objects.filter(tipo_evento=tipo_evento).filter(
        descripcion__icontains=query
    )

    datos = [
        {"evento": evento, "foto": FotoEvento.objects.filter(evento=evento).first()}
        for evento in eventos
    ]

    tipo_evento_nombre = f"Eventos de {tipo_evento.nombre}"
    return render(
        request,
        "negocio/eventos/obtener_evento_por_tipo.html",
        {"eventos": datos, "tipo_evento_nombre": tipo_evento_nombre,
         "tipo_evento_id": tipo_evento.id},
    )
