from django import forms
from .models import ReservaEvento, Evento, Eventualidad, Promocion,ReservaServicio

class ReservaEventoForm(forms.ModelForm):
    class Meta:
        model = ReservaEvento
        fields = [
            "cliente",
            "evento",
            "fechalquiler",
            "hora_inicio_reserva_evento",
            "hora_fin_planificada",
            "hora_fin_real_reserva_evento",
            "costo_alquiler",
            "calificacion_cliente",
            "calificacion_negocio",
            "observacion",
            "estado_alquiler",
        ]
        labels = {
            "cliente": "Cliente",
            "evento": "Evento",
            "fechalquiler": "Fecha de alquiler",
            "hora_inicio_reserva_evento": "Hora de inicio de la reserva",
            "hora_fin_planificada": "Hora de fin planificada",
            "hora_fin_real_reserva_evento": "Hora de fin real de la reserva",
            "costo_alquiler": "Costo del alquiler",
            "calificacion_cliente": "Calificación del cliente",
            "calificacion_negocio": "Calificación del negocio",
            "observacion": "Observación",
            "estado_alquiler": "Estado del alquiler",
        }
        widgets = {
            "observacion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "fechalquiler": forms.DateInput(attrs={"type": "date"}),
        }


class ReservaServicioForm(forms.ModelForm):
    class Meta:
        model = ReservaServicio
        fields = ["alquiler", "servicio", "cantidad"]
        labels = {
            "alquiler": "Reserva del evento",
            "servicio": "Servicio",
            "cantidad": "Cantidad",
        }


class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = [
            "descripcion",
            "porcentaje_descuento",
            "fecha_inicio",
            "fecha_fin",
            "alquiler",
        ]
        labels = {
            "descripcion": "Descripción de la promoción",
            "porcentaje_descuento": "Porcentaje de descuento",
            "fecha_inicio": "Fecha de inicio",
            "fecha_fin": "Fecha de fin",
            "alquiler": "Reserva del evento",
        }
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }


class EventualidadForm(forms.ModelForm):
    class Meta:
        model = Eventualidad
        fields = ["descripcion", "fecha_eventualidad", "alquiler"]
        labels = {
            "descripcion": "Descripción de la eventualidad",
            "fecha_eventualidad": "Fecha de la eventualidad",
            "alquiler": "Reserva del evento",
        }
        widgets = {
            "fecha_eventualidad": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
