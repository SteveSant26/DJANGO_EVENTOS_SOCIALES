from django.shortcuts import render
from django.http import Http404
from ..models import Evento, FotoEvento

from ..forms import *
# Vista para la página de inicio

def listar_eventos(request):
    eventos = Evento.objects.all() 
    return render(request, 'negocio/lista_eventos.html', {'eventos': eventos})  

def obtener_evento(request, evento_id):
    evento = Evento.objects.get(pk=evento_id)
    try:
        evento = Evento.objects.get(pk=evento_id)
    except Evento.DoesNotExist:
        raise Http404("El evento no existe")
    return render(request, 'negocio/obtener_evento.html', {'evento': evento})

def obtener_dar_calificacion(request, evento_id):
    evento = Evento.objects.get(pk=evento_id)
    try:
        evento = Evento.objects.get(pk=evento_id)
    except Evento.DoesNotExist:
        raise Http404("El evento no existe")
    
    if request.method == 'POST':
        calificacion = request.POST['calificacion']
        evento.calificacion = calificacion
        evento.save()
        return render(request, 'negocio/obtener_dar_calificacion.html', {'evento': evento, 'mensaje': 'Calificación guardada'})

    return render(request, 'negocio/obtener_dar_calificacion.html', {'evento': evento})

def listar_fotos_evento(request, evento_id):
    evento = Evento.objects.get(pk=evento_id)
    fotos = FotoEvento.objects.filter(evento=evento)
    return render(request, 'negocio/listar_fotos_evento.html', {'fotos': fotos})


