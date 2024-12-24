from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Negocio


class NegocioResource(resources.ModelResource):
    class Meta:
        model = Negocio


@admin.register(Negocio)
class NegocioAdmin(ImportExportModelAdmin):
    resource_class = NegocioResource
    list_display = (
        "nombre_negocio",
        "logo_negocio",
        "logo_negocio_preview",
        "direccion_negocio",
        "correo_negocio",
        "telefono_negocio",
    )

    def logo_negocio_preview(self, obj):
        if obj.logo_negocio:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(
                    obj.logo_negocio.url
                )
            )
        else:
            return "(No image)"

    logo_negocio_preview.short_description = "Preview"
