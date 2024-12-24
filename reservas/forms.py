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
            "promociones": forms.Select(
                attrs={"queryset": Promocion.objects.all(), "required": False}
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


class ReservaEventoConfirmForm(forms.ModelForm):
    class Meta:
        model = ReservaEvento
        fields = ["codigo_confirmacion_reserva"]
        labels = {
            "codigo_confirmacion_reserva": "Código de Confirmación",
        }

    def __init__(self, *args, **kwargs):
        self.reserva = kwargs.pop('reserva', None)  # Recibir el objeto reserva
        super().__init__(*args, **kwargs)

    def clean_codigo_confirmacion_reserva(self):
        codigo = self.cleaned_data.get('codigo_confirmacion_reserva')
        # Puedes realizar validaciones adicionales con el objeto reserva
        if self.reserva and self.reserva.codigo_confirmacion_reserva != codigo:
            raise forms.ValidationError("El código de confirmación no coincide con la reserva.")
        return codigo
