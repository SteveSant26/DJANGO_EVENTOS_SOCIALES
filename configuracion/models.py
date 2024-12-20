from django.db import models
from django.core.exceptions import ValidationError


class Negocio(models.Model):
    nombre_negocio = models.CharField(max_length=100, verbose_name="Nombre del Negocio")
    direccion_negocio = models.CharField(
        max_length=200, verbose_name="Dirección del Negocio"
    )
    correo_negocio = models.EmailField(verbose_name="Correo del Negocio")
    telefono_negocio = models.CharField(
        max_length=15, verbose_name="Teléfono del Negocio"
    )
    pagina_web_negocio = models.URLField(
        blank=True, null=True, verbose_name="Página Web del Negocio"
    )
    red_social_facebook_negocio = models.URLField(
        blank=True, null=True, verbose_name="Facebook del Negocio"
    )
    red_social_x_negocio = models.URLField(
        blank=True, null=True, verbose_name="X del Negocio"
    )
    red_social_instagram_negocio = models.URLField(
        blank=True, null=True, verbose_name="Instagram del Negocio"
    )
    red_social_twitter_negocio = models.URLField(
        blank=True, null=True, verbose_name="Twitter del Negocio"
    )
    nombre_banco = models.CharField(max_length=100, verbose_name="Nombre del Banco")
    numero_cuenta_banco = models.CharField(
        max_length=100, verbose_name="Número de Cuenta del Banco"
    )
    nombre_propietario_cuenta = models.CharField(
        max_length=100, verbose_name="Nombre del Propietario de la Cuenta"
    )

    def save(self, *args, **kwargs):
        if not self.pk and Negocio.objects.exists():
            raise ValidationError("Solo se puede crear una configuración de negocio.")
        return super(Negocio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_negocio

    class Meta:
        verbose_name = "Informacion del Negocio"
        verbose_name_plural = "Informacion del Negocio"
