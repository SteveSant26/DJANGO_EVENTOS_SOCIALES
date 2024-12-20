from django.contrib import admin
from semantic_admin.admin import SemanticModelAdmin, SemanticTabularInline
from django.utils.safestring import mark_safe

# Register your models here.
from .models import (
    ReservaServicio,
    ReservaEvento,
    Promocion,
    Eventualidad,
    FotoReservaEvento,
)


class PrevisualizacionImagen:
    readonly_fields = ("previsualizacion_imagen",)

    def previsualizacion_imagen(self, obj):
        if obj.imagen:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(
                    obj.imagen.url
                )
            )
        else:
            return "(No image)"

    previsualizacion_imagen.short_description = "Imagen"


class FotoReservaEventoInline(SemanticTabularInline, PrevisualizacionImagen):
    model = FotoReservaEvento
    extra = 1
    fields = ['imagen', 'previsualizacion_imagen']  
    readonly_fields = ['previsualizacion_imagen']


class EventualidadInline(SemanticTabularInline):
    model = Eventualidad
    extra = 1
    fields = ['descripcion', 'fecha_eventualidad', 'alquiler']  


class ReservaServicioInline(SemanticTabularInline):
    model = ReservaServicio
    extra = 1
    fields = ['servicio', 'cantidad']

@admin.register(FotoReservaEvento)
class FotoReservaEventoAdmin(SemanticModelAdmin, PrevisualizacionImagen):
    list_display = ("reserva_evento", "descripcion", "numero_likes", "previsualizacion_imagen")
    search_fields = ("reserva_evento__id",)
    ordering = ("reserva_evento",)
    list_per_page = 10

@admin.register(ReservaServicio)
class ReservaServicioAdmin(SemanticModelAdmin):
    list_display = ("id", "reserva", "servicio", "cantidad")
    list_filter = ("reserva", "servicio")
    search_fields = ("reserva__cliente__username", "servicio__nombre")
    list_per_page = 10  



@admin.register(ReservaEvento)
class ReservaEventoAdmin(SemanticModelAdmin):
    list_display = (
        "id",
        "cliente",
        "evento",
        "hora_inicio_reserva_evento",
        "hora_fin_real_reserva_evento",
        "costo_alquiler",
    )
    list_filter = ("hora_inicio_reserva_evento", "hora_fin_real_reserva_evento")
    search_fields = (
        "cliente__username",
        "hora_inicio_reserva_evento",
        "hora_fin_real_reserva_evento",
    )
    list_per_page = 10
    inlines = [FotoReservaEventoInline, EventualidadInline, ReservaServicioInline]


@admin.register(Promocion)
class PromocionAdmin(SemanticModelAdmin):
    list_display = (
        "id",
        "nombre",
        "descripcion",
        "porcentaje_descuento",
        "fecha_inicio",
        "fecha_fin",
    )
    list_per_page = 10
    list_filter = ("fecha_inicio", "fecha_fin")
    search_fields = ("descripcion", "porcentaje_descuento")


@admin.register(Eventualidad)
class EventualidadAdmin(SemanticModelAdmin):
    list_display = ("id", "descripcion", "fecha_eventualidad", "alquiler")
    list_filter = ("fecha_eventualidad",)
    search_fields = ("descripcion", "fecha_eventualidad", "alquiler__evento__nombre")
    list_per_page = 10
