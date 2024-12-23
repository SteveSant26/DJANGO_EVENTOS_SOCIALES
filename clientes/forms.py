from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from utils.email_service import EmailService
from .models import InformacionCliente

STYLE = "inputs"

class CrearClienteForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar Contraseña",
        }
        widgets = {
            "username": forms.TextInput(attrs={ "class": STYLE}),
            "email": forms.EmailInput(attrs={ "class": STYLE}),
            "password1": forms.PasswordInput(attrs={"class": STYLE}),
            "password2": forms.PasswordInput(attrs={ "class": STYLE}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isalnum():
            raise forms.ValidationError("El nombre de usuario solo puede contener letras y números.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está en uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        cliente_data = {
            "cliente": user,
            "correo": self.cleaned_data.get("email"),
        }
        cliente = InformacionCliente.objects.create(**cliente_data)
        cliente.generar_codigo_verificacion()
        EmailService.enviar_codigo_verificacion(cliente)
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
        labels = {
            "username": "Usuario",
            "password": "Contraseña",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Ingrese su usuario"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("El usuario no existe.", code="username_not_found")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError("La contraseña es incorrecta.", code="invalid_password")
        return password

class VerificarCorreoForm(forms.Form):
    codigo_verificacion = forms.CharField(
        label="Código de verificación",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese el código de verificación"}),
    )

    class Meta:
        fields = ("codigo_verificacion",)

    def clean(self):
        cleaned_data = super().clean()
        codigo_verificacion = cleaned_data.get("codigo_verificacion")
        user = self.user
        perfil = InformacionCliente.objects.filter(usuario=user).first()

        if not perfil:
            raise forms.ValidationError("No se encontró una información del cliente asociada a este usuario.")

        if perfil.codigo_verificacion != codigo_verificacion:
            raise forms.ValidationError("El código de verificación es incorrecto.")

        if perfil.verificado:
            raise forms.ValidationError("Este correo ya ha sido verificado.")

        return cleaned_data

    def save(self):
        perfil = InformacionCliente.objects.get(usuario=self.user)
        perfil.verificado = True
        perfil.save()
        return perfil


class ActualizarClienteForm(forms.ModelForm):
    class Meta:
        model = InformacionCliente
        fields = [
            "nacionalidad",
            "telefono",
            "nombres",
            "apellidos",
            "genero",
            "fecha_nacimiento",
        ]
        labels = {
            "nacionalidad": "Nacionalidad",
            "telefono": "Teléfono",
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "genero": "Género",
            "fecha_nacimiento": "Fecha de nacimiento",
        }
        widgets = {
            "nacionalidad": forms.TextInput(attrs={"required": "required"}),
            "telefono": forms.TextInput(attrs={"required": "required"}),
            "nombres": forms.TextInput(attrs={"required": "required"}),
            "apellidos": forms.TextInput(attrs={"required": "required"}),
            "genero": forms.Select(attrs={"required": "required"}),
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date", "required": "required"}),
        }

    def clean_identificacion_cliente(self):
        identificacion_cliente = self.cleaned_data.get("numero_identificacion")
        if identificacion_cliente != self.instance.numero_identificacion:
            raise forms.ValidationError("No puedes cambiar tu número de identificación.")
        return identificacion_cliente

    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data.get("correo")
        if correo_electronico != self.instance.correo:
            raise forms.ValidationError("No puedes cambiar tu correo electrónico.")
        return correo_electronico
