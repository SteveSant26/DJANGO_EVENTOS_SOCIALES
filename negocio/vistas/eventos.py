from django.shortcuts import render
from django.http import Http404
from ..models import Evento, FotoEvento
from ..forms import ResenaEventoForm

from ..forms import *

# Vista para la página de inicio


def listar_eventos(request):
    eventos = Evento.objects.all()

    datos = []
    for evento in eventos:
        datos.append({"evento": evento, "foto": FotoEvento.objects.filter(evento=evento).first()})
    return render(request, "negocio/eventos/index.html", {"eventos": datos})


def obtener_evento(request, evento_id):
    evento = Evento.objects.get(pk=evento_id)
    try:
        evento = Evento.objects.get(pk=evento_id)
        fotos = FotoEvento.objects.filter(evento=evento)
    except Evento.DoesNotExist:
        raise Http404("El evento no existe")
    return render(request, "negocio/eventos/obtener_evento.html", {"evento": evento, "fotos": fotos})


def obtener_dar_calificacion(request, evento_id):
    evento = Evento.objects.get(pk=evento_id)
    try:
        evento = Evento.objects.get(pk=evento_id)
    except Evento.DoesNotExist:
        raise Http404("El evento no existe")

    if request.method == "POST":
        form = ResenaEventoForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.evento = evento
            resena.save()
            return render(request, "negocio/obtener_evento.html", {"evento": evento})
    else:
        form = ResenaEventoForm()
    return render(request, "negocio/dar_calificacion.html", {"form": form})


def listar_fotos_evento(request, evento_id):
    evento = Evento.objects.get(pk=evento_id)
    fotos = FotoEvento.objects.filter(evento=evento)
    return render(request, "negocio/listar_fotos_evento.html", {"fotos": fotos})
