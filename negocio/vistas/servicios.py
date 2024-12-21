from django.shortcuts import render
from django.http import Http404
from ..models import Servicio, FotoServicio

from ..forms import ResenaServicioForm

# Vista para la página de inicio


def listar_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, "negocio/lista_servicios.html", {"servicios": servicios})


def obtener_servicio(request, servicio_id):
    servicio = Servicio.objects.get(pk=servicio_id)
    try:
        servicio = servicio.objects.get(pk=servicio_id)
    except Servicio.DoesNotExist:
        raise Http404("El servicio no existe")
    return render(request, "negocio/obtener_servicio.html", {"servicio": servicio})


def obtener_dar_calificacion(request, servicio_id):
    try:
        servicio = Servicio.objects.get(pk=servicio_id)
    except Servicio.DoesNotExist:
        raise Http404("El servicio no existe")

    if request.method == "POST":
        form = ResenaServicioForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.servicio = servicio
            resena.save()
            return render(
                request, "negocio/obtener_servicio.html", {"servicio": servicio}
            )
    else:
        form = ResenaServicioForm()
    return render(request, "negocio/dar_calificacion.html", {"form": form})


def listar_fotos_servicio(request, servicio_id):
    servicio = Servicio.objects.get(pk=servicio_id)
    fotos = FotoServicio.objects.filter(servicio=servicio)
    return render(request, "negocio/listar_fotos_servicio.html", {"fotos": fotos})
