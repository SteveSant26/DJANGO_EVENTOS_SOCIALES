from django import forms
from .models import ReservaEvento, ReservaEventoServicio, Promocion
from negocio.models import Evento, Servicio


class ReservaEventoForm(forms.ModelForm):
    class Meta:
        model = ReservaEvento
        fields = [
            "fechalquiler",
            "hora_inicio_reserva_evento",
            "hora_fin_planificada",
            "promociones",
        ]
        labels = {
            "fechalquiler": "Fecha de alquiler",
            "hora_inicio_reserva_evento": "Hora de inicio de la reserva",
            "hora_fin_planificada": "Hora de fin planificada",
            "promociones": "Promoción",
        }
        widgets = {
            "hora_inicio_reserva_evento": forms.TimeInput(attrs={"type": "time"}),
            "hora_fin_planificada": forms.TimeInput(attrs={"type": "time"}),
            "fechalquiler": forms.DateInput(attrs={"type": "date"}),
            "promociones": forms.SelectMultiple(
                attrs={"required": False}
            ),
        }


class ReservaEventoServicioForm(forms.ModelForm):

    class Meta:
        model = ReservaEventoServicio
        fields = ["servicio", "cantidad"]
        labels = {
            "servicio": "Servicio",
            "cantidad": "Cantidad",
        }
        widgets = {
            "cantidad": forms.NumberInput(attrs={"required": False}),
            "servicio": forms.Select(
                attrs={"queryset": Servicio.objects.all(), "required": False}
            ),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if not cantidad:
            raise forms.ValidationError("Este campo es requerido al guardar.")
        return cantidad


class ReservaEventoConfirmForm(forms.Form):
    codigo_confirmacion_reserva = forms.CharField(
        label="Código de confirmación",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese el código de confirmación"}),
    )


    def __init__(self, *args, **kwargs):
        
        self.reserva_evento = kwargs.pop('reserva', None)  
        super().__init__(*args, **kwargs)  

    def clean(self):
        cleaned_data = super().clean()
        codigo_confirmacion_reserva = cleaned_data.get("codigo_confirmacion_reserva")

        if not self.reserva_evento:
            raise forms.ValidationError("No se encontró la reserva del evento")

        
        if str(self.reserva_evento.codigo_confirmacion_reserva) != str(codigo_confirmacion_reserva):
            raise forms.ValidationError("El código de confirmación es incorrecto.")

        
        if self.reserva_evento.fue_confirmada:
            raise forms.ValidationError("Este alquiler ya ha sido confirmado.")

        return cleaned_data
    
    
    def save(self):
        
        self.reserva_evento.fue_confirmada = True
        self.reserva_evento.estado_reserva = ReservaEvento.ESTADOS_ALQUILER[2][0]
        self.reserva_evento.save()
        return self.reserva_evento