from django.contrib import admin

# Register your models here.
from .models import ReservaServicio, ReservaEvento, Promocion, Eventualidad


admin.site.register(ReservaServicio)
admin.site.register(ReservaEvento)
admin.site.register(Promocion)
admin.site.register(Eventualidad)