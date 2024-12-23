from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import InformacionCliente


class InformacionClienteResource(resources.ModelResource):
    class Meta:
        model = InformacionCliente


# Register the model with the admin
@admin.register(InformacionCliente)
class InformacionClienteAdmin(ImportExportModelAdmin):
    resource_class = InformacionClienteResource
    list_display = (
        "cliente",
        "nombres",
        "apellidos",
        "telefono",
        "correo",
        "numero_identificacion",
        "fecha_registro",
    )
    search_fields = (
        "cliente__username",
        "apellidos",
        "telefono",
        "correo",
        "numero_identificacion",
        "fecha_registro",
    )
    list_filter = ("fecha_registro", "genero", "verificado")
    ordering = ("fecha_registro",)
    list_per_page = 10
