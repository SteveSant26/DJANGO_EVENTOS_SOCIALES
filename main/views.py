from django.shortcuts import render
<<<<<<< HEAD
from negocio.models import TipoEvento
# Create your views here.
def home_view(request):
    tipoEventos = TipoEvento.objects.all()[:3]
    return render(request, 'main/home.html', {"tipoEventos": tipoEventos})
=======
from django.db import models
from negocio.models import Evento


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

    return render(
        request, "main/home.html", {"eventos_mas_populares": eventos_mas_populares}
    )
>>>>>>> efe6633859bc3e8e6b75074cde5c429080a64af0
