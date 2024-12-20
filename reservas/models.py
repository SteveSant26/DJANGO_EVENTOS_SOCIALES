from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.db import models
from utils.abstract_model import BaseModel
from negocio.models import Evento, Servicio


class ReservaEvento(BaseModel):
    class Meta:
        verbose_name = "Reserva de evento"
        verbose_name_plural = "Reservas de eventos"
        
        
    ESTADOS_ALQUILER = [
        ("Activo", "Activo"),
        ("Cancelado", "Cancelado"),
        ("Pendiente", "Pendiente"),
        ("Confirmado", "Confirmado"),
        ("Finalizado", "Finalizado"),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cliente")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    fechalquiler = models.DateField(verbose_name="Fecha de alquiler")
    hora_inicio_reserva_evento = models.TimeField(
        verbose_name="Hora de inicio de la reserva"
    )
    hora_fin_planificada = models.TimeField(verbose_name="Hora de fin planificada")
    hora_fin_real_reserva_evento = models.TimeField(
        blank=True, null=True, verbose_name="Hora de fin real de la reserva"
    )
    costo_alquiler = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Costo del alquiler"
    )
    calificacion_cliente = models.IntegerField(
        blank=True, null=True, verbose_name="Calificación del cliente"
    )
    calificacion_negocio = models.IntegerField(
        blank=True, null=True, verbose_name="Calificación del negocio"
    )
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")
    estado_alquiler = models.CharField(
        max_length=20,
        choices=ESTADOS_ALQUILER,
        default="Pendiente",
        verbose_name="Estado del alquiler",
    )

    codigo_confirmacion_reserva = models.CharField(
        max_length=20, verbose_name="Código de la reserva", unique=True
    )
    
    def crear_codigo_confirmacion(self):
        self.codigo_confirmacion_reserva = get_random_string(length=6)
        self.save()
        return self.codigo_confirmacion_reserva

    def __str__(self):
        return f"Alquiler {self.pk} - Cliente: {self.cliente}"


class ReservaServicio(BaseModel):
    class Meta:
        verbose_name = "Reserva de servicio"
        verbose_name_plural = "Reservas de servicios"
    reserva = models.ForeignKey(
        ReservaEvento, on_delete=models.CASCADE, verbose_name="Reserva del evento"
    )
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, verbose_name="Servicio"
    )
    cantidad = models.IntegerField(verbose_name="Cantidad")

    def __str__(self):
        return f"Servicio {self.servicio.descripcion} para Alquiler {self.reserva.pk}"


class Promocion(BaseModel):
    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        
    descripcion = models.CharField(
        max_length=200, verbose_name="Descripción de la promoción"
    )
    porcentaje_descuento = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Porcentaje de descuento"
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de fin")
    alquiler = models.ForeignKey(
        ReservaEvento, on_delete=models.CASCADE, verbose_name="Reserva del evento"
    )

    def __str__(self):
        return f"Promoción {self.descripcion} ({self.porcentaje_descuento}%)"


class Eventualidad(BaseModel):
    class Meta:
        verbose_name = "Eventualidad"
        verbose_name_plural = "Eventualidades"
    descripcion = models.TextField(verbose_name="Descripción de la eventualidad")
    fecha_eventualidad = models.DateField(verbose_name="Fecha de la eventualidad")
    alquiler = models.ForeignKey(
        ReservaEvento, on_delete=models.CASCADE, verbose_name="Reserva del evento"
    )

    def __str__(self):
        return f"Eventualidad {self.pk} - {self.descripcion}"
