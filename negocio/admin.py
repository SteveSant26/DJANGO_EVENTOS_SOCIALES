from django.contrib import admin
from .models import ( TipoEvento, Evento,Servicio,FotoEvento, FotoServicio
)

admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(Servicio)
admin.site.register(FotoEvento)
admin.site.register(FotoServicio)
