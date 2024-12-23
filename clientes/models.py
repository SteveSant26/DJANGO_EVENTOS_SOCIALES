from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User


class InformacionClienteManager(models.Manager):
    def get_or_create(self, defaults = ..., **kwargs):
        if self.filter(cliente=kwargs.get("cliente")).exists():
            return self.get(cliente=kwargs.get("cliente"))
        return self.create(**kwargs)

class InformacionCliente(models.Model):
    cliente = models.OneToOneField(User, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    numero_identificacion = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nacionalidad = models.CharField(max_length=50,blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    telefono = models.CharField(max_length=15,blank=True, null=True)
    nombres = models.CharField(max_length=100,blank=True, null=True)
    apellidos = models.CharField(max_length=100,blank=True, null=True)
    correo = models.EmailField()
    fecha_nacimiento = models.DateField(blank=True, null=True)

    genero = models.CharField(
        max_length=10,
        choices=[("Masculino", "Masculino"), ("Femenino", "Femenino"), ("Otro", "Otro")],
    )
    codigo_verificacion = models.CharField(max_length=6, blank=True, null=True)
    verificado = models.BooleanField(default=False)
    
    
    
    
    def generar_codigo_verificacion(self):
        self.codigo_verificacion = get_random_string(length=6, allowed_chars="1234567890")
        return self.codigo_verificacion

    def save(self, *args, **kwargs):
        from utils.email_service import EmailService
        
        if not self.codigo_verificacion:
            self.generar_codigo_verificacion()
        EmailService.enviar_codigo_verificacion(self)

        super().save( *args, **kwargs)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"