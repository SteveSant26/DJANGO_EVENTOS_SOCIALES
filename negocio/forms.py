from django import forms
from .models import (
    TipoEvento,
    Evento,
    Servicio,
    FotoEvento,
    FotoServicio,
)


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = ["nombre"]
        labels = {
            "nombre": "Nombre del tipo de evento",
        }


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            "descripcion",
            "valor_referencial",
            "numero_horas_permitidas",
            "valor_extra_hora",
            "tipo_evento",
        ]
        labels = {
            "descripcion": "Descripción del evento",
            "valor_referencial": "Valor referencial",
            "numero_horas_permitidas": "Número de horas permitidas",
            "valor_extra_hora": "Valor extra por hora",
            "tipo_evento": "Tipo de evento",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ["descripcion", "valor_por_unidad"]
        labels = {
            "descripcion": "Descripción del servicio",
            "valor_por_unidad": "Valor por unidad",
        }


class FotoEventoForm(forms.ModelForm):
    class Meta:
        model = FotoEvento
        fields = ["imagen", "evento"]
        labels = {
            "imagen": "Imagen del evento",
            "evento": "Evento",
        }


class FotoServicioForm(forms.ModelForm):
    class Meta:
        model = FotoServicio
        fields = ["imagen", "servicio"]
        labels = {
            "imagen": "Imagen del servicio",
            "servicio": "Servicio",
        }
