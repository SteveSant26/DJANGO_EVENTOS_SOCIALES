from django.contrib import admin
from semantic_admin.admin import SemanticModelAdmin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import Negocio


@admin.register(Negocio)
class NegocioAdmin(SemanticModelAdmin):
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
                return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.logo_negocio.url))
            else:
                return '(No image)'

    logo_negocio_preview.short_description = 'Preview'