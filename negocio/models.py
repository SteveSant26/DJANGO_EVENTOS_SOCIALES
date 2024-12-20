from django.db import models
from utils.abstract_model import BaseModel


class TipoEvento(BaseModel):
    class Meta:
        verbose_name = "Tipo de evento"
        verbose_name_plural = "Tipos de eventos"
    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombre del tipo de evento"
    )

    def __str__(self):
        return self.nombre


class Evento(BaseModel):
    verbose_name = "Evento"
    verbose_name_plural = "Eventos"
    descripcion = models.TextField(
        verbose_name="Descripción del evento"
    )
    valor_referencial = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor referencial"
    )
    numero_horas_permitidas = models.IntegerField(
        verbose_name="Número de horas permitidas"
    )
    valor_extra_hora = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor extra por hora"
    )
    tipo_evento = models.ForeignKey(
        TipoEvento, 
        on_delete=models.CASCADE, 
        verbose_name="Tipo de evento"
    )

    def __str__(self):
        return f"{self.descripcion} ({self.tipo_evento.nombre})"



class Servicio(BaseModel):
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    descripcion = models.CharField(
        max_length=200, 
        verbose_name="Descripción del servicio"
    )
    valor_por_unidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor por unidad"
    )

    def __str__(self):
        return self.descripcion


class FotoEvento(BaseModel):
    class Meta:
        verbose_name = "Foto de evento"
        verbose_name_plural = "Fotos de eventos"
    imagen = models.ImageField(
        upload_to="eventos/imagenes/", 
        verbose_name="Imagen del evento"
    )
    evento = models.ForeignKey(
        Evento, 
        on_delete=models.CASCADE, 
        verbose_name="Evento"
    )

    def __str__(self):
        return f"Foto de Evento {self.evento.descripcion}"


class FotoServicio(BaseModel):
    class Meta:
        verbose_name = "Foto de servicio"
        verbose_name_plural = "Fotos de servicios"
    imagen = models.ImageField(
        upload_to="servicios/imagenes/", 
        verbose_name="Imagen del servicio"
    )
    servicio = models.ForeignKey(
        Servicio, 
        on_delete=models.CASCADE, 
        verbose_name="Servicio"
    )

    def __str__(self):
        return f"Foto de Servicio {self.servicio.descripcion}"
