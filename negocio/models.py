from django.db import models
from cloudinary.models import CloudinaryField
from utils.abstract_model import BaseModel
from django.contrib.auth.models import User



## EVENTOS
class TipoEvento(BaseModel):
    class Meta:
        verbose_name = "Tipo de evento"
        verbose_name_plural = "Tipos de eventos"

    nombre = models.CharField(max_length=100, verbose_name="Nombre del tipo de evento")
    descripcion = models.TextField(
        verbose_name="Descripción del tipo de evento", blank=True, null=True
    )

    def __str__(self):
        return self.nombre


class Evento(BaseModel):
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    nombre = models.CharField(max_length=100, verbose_name="Nombre del evento")
    descripcion = models.TextField(verbose_name="Descripción del evento")
    valor_referencial = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor referencial"
    )
    numero_horas_permitidas = models.IntegerField(
        verbose_name="Número de horas permitidas"
    )
    valor_extra_hora = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor extra por hora"
    )
    tipo_evento = models.ForeignKey(
        TipoEvento, on_delete=models.CASCADE, verbose_name="Tipo de evento"
    )

    def __str__(self):
        return self.nombre


class FotoEvento(BaseModel):
    class Meta:
        verbose_name = "Foto de evento"
        verbose_name_plural = "Fotos de eventos"

    imagen = CloudinaryField(
        "imagen",
    )
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    descripcion = models.TextField(
        verbose_name="Descripción de la foto", blank=True, null=True
    )
    numero_likes = models.IntegerField(default=0, verbose_name="Número de likes")


    def __str__(self):
        return f"Foto de Evento {self.evento.descripcion}"



class ResenasEvento(BaseModel):
    class Meta:
        verbose_name = "Reseña de evento"
        verbose_name_plural = "Reseñas de eventos"

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    calificacion = models.IntegerField(verbose_name="Calificación")
    comentario = models.TextField(verbose_name="Comentario", blank=True, null=True)

    def __str__(self):
        return f"Reseña de evento {self.evento.descripcion}"
    
    
## SERVICIOS

class Servicio(BaseModel):
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    nombre = models.CharField(max_length=100, verbose_name="Nombre del servicio")
    descripcion = models.CharField(
        max_length=200, verbose_name="Descripción del servicio"
    )
    valor_por_unidad = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor por unidad"
    )
    estado = models.BooleanField(default=True, verbose_name="Estado del servicio")

    def __str__(self):
        return self.nombre



class FotoServicio(BaseModel):
    class Meta:
        verbose_name = "Foto de servicio"
        verbose_name_plural = "Fotos de servicios"

    imagen = CloudinaryField(
        "imagen",
    )
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, verbose_name="Servicio"
    )
    descripcion = models.TextField(
        verbose_name="Descripción de la foto", blank=True, null=True
    )
    numero_likes = models.IntegerField(default=0, verbose_name="Número de likes")

    def __str__(self):
        return f"Foto de Servicio {self.servicio.descripcion}"

class ResenasServicio(BaseModel):
    class Meta:
        verbose_name = "Reseña de servicio"
        verbose_name_plural = "Reseñas de servicios"

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, verbose_name="Servicio")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    calificacion = models.IntegerField(verbose_name="Calificación")
    comentario = models.TextField(verbose_name="Comentario", blank=True, null=True)

    def __str__(self):
        return f"Reseña de servicio {self.servicio.descripcion}"