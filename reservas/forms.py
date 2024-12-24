from django import forms
from .models import ReservaEvento, ReservaEventoServicio
from negocio.models import Evento, Servicio


class ReservaEventoForm(forms.ModelForm):
    class Meta:
        model = ReservaEvento
        fields = [
            "fechalquiler",
            "hora_inicio_reserva_evento",
            "hora_fin_planificada",
            "promociones"
        ]
        labels = {
            "fechalquiler": "Fecha de alquiler",
            "hora_inicio_reserva_evento": "Hora de inicio de la reserva",
            "hora_fin_planificada": "Hora de fin planificada",
        }
        widgets = {

            "hora_inicio_reserva_evento": forms.TimeInput(attrs={"type": "time"}),
            "hora_fin_planificada": forms.TimeInput(attrs={"type": "time"}),
            "fechalquiler": forms.DateInput(attrs={"type": "date"}),
        }

    # def save(self, commit=True):
    #     reserva = super().save(commit=False)
    #     if commit:
    #         reserva.save()

    #     return reserva


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
