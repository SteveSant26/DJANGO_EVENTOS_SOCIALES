from django import forms

from .models import InformacionCliente

STYLE = "inputs"


class VerificarCorreoForm(forms.Form):
    codigo_verificacion_correo = forms.CharField(
        label="Código de verificación",
        widget=forms.TextInput(),
    )

    class Meta:
        fields = ("codigo_verificacion_correo",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Obtener el usuario pasado al formulario
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        codigo_verificacion = cleaned_data.get("codigo_verificacion_correo")
        

        if not codigo_verificacion:
            raise forms.ValidationError("El código de verificación no puede estar vacío.")
        
        user = self.user
        perfil = InformacionCliente.objects.filter(cliente=user).first()

        if not perfil:
            raise forms.ValidationError(
                "No se encontró una información del cliente asociada a este usuario."
            )

        if perfil.codigo_verificacion != codigo_verificacion:
            raise forms.ValidationError("El código de verificación no es válido.")

        return cleaned_data



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = InformacionCliente
        fields = [
            "nacionalidad",
            "descripcion",
            "telefono",
            "nombres",
            "apellidos",
            "genero",
            "fecha_nacimiento",
        ]
        labels = {
            "nacionalidad": "Nacionalidad",
            "descripcion": "Descripción",
            "telefono": "Teléfono",
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "genero": "Género",
            "fecha_nacimiento": "Fecha de nacimiento",
        }
        widgets = {
            "nacionalidad": forms.TextInput(attrs={"required": "required"}),
            "descripcion": forms.TextInput(attrs={"required": "required"}),
            "telefono": forms.TextInput(attrs={"required": "required"}),
            "nombres": forms.TextInput(attrs={"required": "required"}),
            "apellidos": forms.TextInput(attrs={"required": "required"}),
            "genero": forms.Select(attrs={"required": "required"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "required": "required"}
            ),
        }

    def clean_identificacion_cliente(self):
        identificacion_cliente = self.cleaned_data.get("numero_identificacion")
        if identificacion_cliente != self.instance.numero_identificacion:
            raise forms.ValidationError(
                "No puedes cambiar tu número de identificación."
            )
        return identificacion_cliente

    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data.get("correo")
        if correo_electronico != self.instance.correo:
            raise forms.ValidationError("No puedes cambiar tu correo electrónico.")
        return correo_electronico
