from django.contrib import admin
from semantic_admin.admin import SemanticModelAdmin

# Import your models
from .models import InformacionCliente

# Admin class for InformacionCliente
@admin.register(InformacionCliente)
class InformacionClienteAdmin(SemanticModelAdmin):
    list_display = ("cliente", "nombres", "apellidos", "telefono", "correo", "numero_identificacion", "fecha_registro")
    search_fields = ("cliente__username", "apellidos", "telefono", "correo", "numero_identificacion", "fecha_registro")
    list_filter = ("fecha_registro", "genero", "verificado")
    ordering = ("fecha_registro",)
    list_per_page = 10  
