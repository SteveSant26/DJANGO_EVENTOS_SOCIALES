from django.db import models


class BaseModel(models.Model):
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de creación"
    )
    ultima_actualizacion = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última actualización"
    )

    class Meta:
        abstract = True