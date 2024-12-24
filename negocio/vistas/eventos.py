from django.shortcuts import render, get_object_or_404
from django.http import Http404
from ..models import Evento, FotoEvento, TipoEvento
from ..forms import ResenaEventoForm


def listar_eventos(request):
    eventos = Evento.objects.all()
    datos = [
        {"evento": evento, "foto": FotoEvento.objects.filter(evento=evento).first()}
        for evento in eventos
    ]
    return render(request, "negocio/eventos/index.html", {"eventos": datos})


def obtener_evento(request, evento_id):
    
    evento = get_object_or_404(Evento, pk=evento_id)
    fotos = FotoEvento.objects.filter(evento=evento)
    
    nombreEvento = f"Evento #{evento.id}"
    return render(
        request,
        "negocio/eventos/obtener_evento.html",
        {"evento": evento, "fotos": fotos, "nombreEvento": nombreEvento},
    )


def obtener_dar_calificacion(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    if request.method == "POST":
        form = ResenaEventoForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.evento = evento
            resena.save()
            
            return render(request, "negocio/eventos/obtener_evento.html", {"evento": evento})
    else:
        form = ResenaEventoForm()

    return render(request, "negocio/dar_calificacion.html", {"form": form, "evento": evento})


def listar_fotos_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    fotos = FotoEvento.objects.filter(evento=evento)
    return render(request, "negocio/listar_fotos_evento.html", {"fotos": fotos})


def listar_tipos_eventos(request):
    tipo_eventos = TipoEvento.objects.all()
    return render(
        request, "negocio/eventos/tipo_eventos.html", {"tipo_eventos": tipo_eventos}
    )


def listar_eventos_por_tipo(request, tipo_evento_id):
    tipo_evento = get_object_or_404(TipoEvento, pk=tipo_evento_id)
    eventos = Evento.objects.filter(tipo_evento=tipo_evento)
    
    datos = [
        {"evento": evento, "foto": FotoEvento.objects.filter(evento=evento).first()}
        for evento in eventos
    ]
    
    tipo_evento_nombre = f"Eventos de {tipo_evento.nombre}"
    return render(
        request,
        "negocio/eventos/obtener_evento_por_tipo.html",
        {"eventos": datos, "tipo_evento_nombre": tipo_evento_nombre},
    )
