from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db import models
from utils.abstract_model import BaseModel
from django.core.exceptions import ValidationError
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

    promociones = models.ManyToManyField(
        "Promocion",
        blank=True,
        verbose_name="Promociones",
    )

    fechalquiler = models.DateField(verbose_name="Fecha de alquiler")
    hora_inicio_reserva_evento = models.TimeField(
        verbose_name="Hora de inicio de la reserva"
    )
    hora_fin_planificada = models.TimeField(verbose_name="Hora de fin planificada")
    hora_fin_real_reserva_evento = models.TimeField(
        blank=True, null=True, verbose_name="Hora de fin real de la reserva"
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
        max_length=20,
        verbose_name="Código de la reserva",
        unique=True,
        blank=True,
        null=True,
    )

    @property
    def costo_alquiler(self):
        costo = self.evento.valor_referencial
        for reserva_servicio in self.reservas_servicios.all():
            costo += reserva_servicio.servicio.precio * reserva_servicio.cantidad

    def crear_codigo_confirmacion(self):
        self.codigo_confirmacion_reserva = get_random_string(length=6)
        self.save()
        return self.codigo_confirmacion_reserva

    def clean(self):
        if self.hora_inicio_reserva_evento >= self.hora_fin_planificada:
            raise ValidationError(
                "La hora de inicio de la reserva debe ser menor a la hora de fin planificada"
            )

    def save(self, *args, **kwargs):
        if not self.codigo_confirmacion_reserva:
            self.crear_codigo_confirmacion()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de evento {self.pk} - Cliente: {self.cliente}"


class FotoReservaEvento(BaseModel):
    class Meta:
        verbose_name = "Foto de reserva de evento"
        verbose_name_plural = "Fotos de reserva de eventos"

    imagen = CloudinaryField(
        "imagen",
    )
    reserva_evento = models.ForeignKey(
        ReservaEvento,
        on_delete=models.CASCADE,
        verbose_name="Reserva del evento",
        related_name="fotos",
    )
    descripcion = models.TextField(
        verbose_name="Descripción de la foto", blank=True, null=True
    )
    numero_likes = models.IntegerField(default=0, verbose_name="Número de likes")

    def __str__(self):
        return f"Foto de Evento {self.reserva_evento}"


class ReservaEventoServicio(BaseModel):
    class Meta:
        verbose_name = "Reserva de servicio"
        verbose_name_plural = "Reservas de servicios"

    reserva = models.ForeignKey(
        ReservaEvento,
        on_delete=models.CASCADE,
        verbose_name="Reserva del evento",
        related_name="reservas_servicios",
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        verbose_name="Servicio",
        related_name="reservas_servicios",
    )
    cantidad = models.IntegerField(verbose_name="Cantidad")


    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")

        if hasattr(self, "reserva") and self.reserva and self.servicio:
            if ReservaEventoServicio.objects.filter(
                reserva=self.reserva, servicio=self.servicio
            ).exists():
                raise ValidationError("El servicio ya ha sido reservado")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Servicio {self.servicio.descripcion} para Alquiler {self.reserva.pk}"


class Promocion(BaseModel):
    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"

    nombre = models.CharField(max_length=100, verbose_name="Nombre de la promoción")
    descripcion = models.CharField(
        max_length=200, verbose_name="Descripción de la promoción"
    )
    porcentaje_descuento = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Porcentaje de descuento"
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de fin")

    def __str__(self):
        return f"{self.nombre}"


class Eventualidad(BaseModel):
    class Meta:
        verbose_name = "Eventualidad"
        verbose_name_plural = "Eventualidades"

    descripcion = models.TextField(verbose_name="Descripción de la eventualidad")
    fecha_eventualidad = models.DateField(
        verbose_name="Fecha de la eventualidad",
    )
    alquiler = models.ForeignKey(
        ReservaEvento, on_delete=models.CASCADE, verbose_name="Reserva del evento"
    )

    def __str__(self):
        return f"Eventualidad {self.pk} - {self.descripcion}"
