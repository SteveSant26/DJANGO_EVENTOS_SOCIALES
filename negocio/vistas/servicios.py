from django.shortcuts import render, redirect
from django.http import Http404
from ..models import Servicio, FotoServicio, ResenaServicio
from django.contrib import messages
from ..forms import ResenaServicioForm

# Vista para la página de inicio


def listar_servicios(request):
    servicios = Servicio.objects.all()

    datos = []
    for servicio in servicios:
        datos.append({"servicio": servicio, "foto": FotoServicio.objects.filter(servicio=servicio).first()})
    return render(request, "negocio/servicios/index.html", {"servicios": datos})


def obtener_servicio(request, servicio_id):
    servicio = Servicio.objects.get(pk=servicio_id)
    fotos = FotoServicio.objects.filter(servicio=servicio)
    resenasServicio = ResenaServicio.objects.filter(servicio=servicio)

    if request.method == "POST":
        formresena = ResenaServicioForm(request.POST)
        if formresena.is_valid():
            
            resena = formresena.save(commit=False)
            resena.servicio = servicio
            resena.autor = request.user
            resena.save()
            messages.success(request, "Reseña creada correctamente.")
            return redirect("negocio:obtener_servicio", servicio_id)
        
    formresena = ResenaServicioForm()
    return render(request, "negocio/servicios/obtener_servicio.html", {"servicio": servicio, "fotos": fotos, "resenasServicio": resenasServicio, "formresena": formresena})


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
