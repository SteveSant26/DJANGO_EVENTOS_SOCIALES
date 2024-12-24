from django import forms
from .models import ReservaEvento, Evento, Eventualidad, Promocion,ReservaEventoServicio

class ReservaEventoForm(forms.ModelForm):
    class Meta:
        model = ReservaEvento
        fields = [
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
            "observacion": forms.TextInput(attrs={"class": "form-control"}),
            "fechalquiler": forms.DateInput(attrs={"type": "date"}),
        }
        
    def save(self, commit=True):
        reserva = super().save(commit=False)
        if commit:
            reserva.save()
        from utils.email_service import EmailService
        EmailService.enviar_codigo_confirmacion(reserva)
        return reserva



class ReservaEventoServicioForm(forms.ModelForm):
    class Meta:
        model = ReservaEventoServicio
        fields = ["reserva", "servicio", "cantidad"]
        labels = {
            "reserva": "Reserva del evento",
            "servicio": "Servicio",
            "cantidad": "Cantidad",
        }


class ReservaEventoConfirmForm(forms.ModelForm):
    class Meta:
        model = ReservaEvento
        fields = ["codigo_confirmacion_reserva"]
        labels = {
            "codigo_confirmacion_reserva": "Código de Confirmación",
        }