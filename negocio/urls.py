# negocio/urls.py
from django.urls import path
from . import vistas


app_name = "negocio"

urlpatterns = [
    path("eventos/", vistas.eventos.listar_eventos, name="listar_eventos"),
    path(
        "eventos/<int:evento_id>/", vistas.eventos.obtener_evento, name="obtener_evento"
    ),
    path(
        "eventos/<int:evento_id>/calificacion/",
        vistas.eventos.obtener_dar_calificacion,
        name="obtener_dar_calificacion",
    ),
    path(
        "eventos/<int:evento_id>/fotos/",
        vistas.eventos.listar_fotos_evento,
        name="listar_fotos_evento",
    ),
    path("servicios/", vistas.servicios.listar_servicios, name="listar_servicios"),
    path(
        "servicios/<int:servicio_id>/",
        vistas.servicios.obtener_servicio,
        name="obtener_servicio",
    ),
    path(
        "servicios/<int:servicio_id>/calificacion/",
        vistas.servicios.obtener_dar_calificacion,
        name="obtener_dar_calificacion_servicio",
    ),
    path(
        "servicios/<int:servicio_id>/fotos/",
        vistas.servicios.listar_fotos_servicio,
        name="listar_fotos_servicio",
    ),
]
