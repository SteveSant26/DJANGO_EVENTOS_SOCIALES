from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    TipoEvento,
    Evento,
    Servicio,
    FotoEvento,
    FotoServicio,
    ResenaEvento,
    ResenaServicio,
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


class TipoEventoResource(resources.ModelResource):
    class Meta:
        model = TipoEvento


class EventoResource(resources.ModelResource):
    class Meta:
        model = Evento


class ServicioResource(resources.ModelResource):
    class Meta:
        model = Servicio


class FotoEventoResource(resources.ModelResource):
    class Meta:
        model = FotoEvento


class FotoServicioResource(resources.ModelResource):
    class Meta:
        model = FotoServicio


class ResenaEventoResource(resources.ModelResource):
    class Meta:
        model = ResenaEvento


class ResenaServicioResource(resources.ModelResource):
    class Meta:
        model = ResenaServicio


# Registro de modelos con import_export
@admin.register(TipoEvento)
class TipoEventoAdmin(ImportExportModelAdmin):
    resource_class = TipoEventoResource
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)
    list_per_page = 10


class FotoEventoInline(admin.TabularInline, PrevisualizacionImagen):
    model = FotoEvento
    extra = 1
    fields = ["imagen", "previsualizacion_imagen"]
    readonly_fields = ["previsualizacion_imagen"]


class ResenasEventoInline(admin.TabularInline):
    model = ResenaEvento
    extra = 1


@admin.register(ResenaEvento)
class ResenaEventoAdmin(ImportExportModelAdmin):
    resource_class = ResenaEventoResource
    list_display = ("evento", "autor", "comentario", "calificacion")
    search_fields = (
        "evento__nombre",
        "autor__username",
        "comentario",
    )
    ordering = ("evento", "autor", "calificacion")


@admin.register(FotoEvento)
class FotoEventoAdmin(ImportExportModelAdmin, PrevisualizacionImagen):
    resource_class = FotoEventoResource
    list_display = ("evento", "descripcion", "numero_likes", "previsualizacion_imagen")
    search_fields = ("evento__nombre",)
    ordering = ("evento",)
    list_per_page = 10


@admin.register(Evento)
class EventoAdmin(ImportExportModelAdmin):
    resource_class = EventoResource
    list_display = (
        "nombre",
        "tipo_evento",
        "descripcion",
        "valor_extra_hora",
        "numero_horas_permitidas",
    )
    search_fields = (
        "nombre",
        "tipo_evento__nombre",
        "descripcion",
        "valor_extra_hora",
        "numero_horas_permitidas",
    )
    list_filter = ("tipo_evento", "valor_extra_hora", "numero_horas_permitidas")
    ordering = ("nombre",)
    inlines = [FotoEventoInline, ResenasEventoInline]
    list_per_page = 10


class FotoServicioInline(admin.TabularInline, PrevisualizacionImagen):
    model = FotoServicio
    extra = 1
    fields = ["imagen", "previsualizacion_imagen"]
    readonly_fields = ["previsualizacion_imagen"]


class ResenaServicioInline(admin.TabularInline):
    model = ResenaServicio
    extra = 1


@admin.register(ResenaServicio)
class ResenaServicioAdmin(ImportExportModelAdmin):
    resource_class = ResenaServicioResource
    list_display = ("servicio", "autor", "comentario", "calificacion")
    search_fields = (
        "servicio__nombre",
        "autor__username",
        "comentario",
    )
    ordering = ("servicio", "autor", "calificacion")


@admin.register(Servicio)
class ServicioAdmin(ImportExportModelAdmin):
    resource_class = ServicioResource
    list_display = ("nombre", "descripcion", "valor_por_unidad", "estado")
    search_fields = ("nombre", "descripcion")
    list_filter = ("estado", "valor_por_unidad")
    ordering = ("nombre", "valor_por_unidad")
    inlines = [FotoServicioInline, ResenaServicioInline]
    list_per_page = 10


@admin.register(FotoServicio)
class FotoServicioAdmin(ImportExportModelAdmin, PrevisualizacionImagen):
    resource_class = FotoServicioResource
    list_display = (
        "servicio",
        "descripcion",
        "numero_likes",
        "previsualizacion_imagen",
    )
    search_fields = ("servicio__nombre",)
    ordering = ("servicio", "numero_likes")
    list_per_page = 10
