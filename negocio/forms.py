from django import forms
from .models import Cliente, Alquiler

# Formulario para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_identificacion', 'nacionalidad', 'fecha_registro', 'telefono', 
                  'nombres', 'apellidos', 'correo', 'genero']
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para Alquiler
class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        exclude = ['costo_alquiler', 'calificacioncliente', 'calificacionnegocio']
        widgets = {
            'fechalquiler': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio_reserva': forms.TimeInput(attrs={'type': 'time'}),
            'horafinplanificada': forms.TimeInput(attrs={'type': 'time'}),
            'estado_alquiler': forms.Select(attrs={'class': 'form-control'}),
        }
