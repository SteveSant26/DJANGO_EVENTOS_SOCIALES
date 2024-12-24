from django.shortcuts import render
from django.db import models
from negocio.models import Evento, TipoEvento


def home_view(request):

    eventos_mas_populares = Evento.objects.annotate(
        numero_resenas=models.Count("resenas_evento")
    ).order_by("-numero_resenas")[:6]

    queryset = []
    for evento in eventos_mas_populares:
        queryset.append({
            "evento": evento,
            "foto": evento.fotoevento_set.first()
        })

    tipo_eventos = TipoEvento.objects.all()[:6]
    return render(
        request, "main/home.html", {"eventos_mas_populares": queryset, "tipo_eventos": tipo_eventos}
    )
