from django.contrib import admin
from .models import (
    Cliente, TipoEvento, Evento, Negocio, Alquiler,
    Servicio, AlquilerServicio, Promocion, Eventualidad,
    FotoEvento, FotoServicio
)

admin.site.register(Cliente)
admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(Negocio)
admin.site.register(Alquiler)
admin.site.register(Servicio)
admin.site.register(AlquilerServicio)
admin.site.register(Promocion)
admin.site.register(Eventualidad)
admin.site.register(FotoEvento)
admin.site.register(FotoServicio)
