from django.db import models

class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    numero_identificacion = models.CharField(max_length=50, unique=True)
    nacionalidad = models.CharField(max_length=50)
    fecha_registro = models.DateField()
    telefono = models.CharField(max_length=15)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    genero = models.CharField(
        max_length=10,
        choices=[("Masculino", "Masculino"), ("Femenino", "Femenino"), ("Otro", "Otro")]
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class TipoEvento(models.Model):
    idtipo_evento = models.AutoField(primary_key=True)
    nombreevento = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreevento


class Evento(models.Model):
    idevento = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    valor_referencial = models.DecimalField(max_digits=10, decimal_places=2)
    numero_horas_permitidas = models.IntegerField()
    valor_extra_hora = models.DecimalField(max_digits=10, decimal_places=2)
    idtipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion


class Negocio(models.Model):
    idnegocio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    pagina_web = models.URLField(blank=True, null=True)
    red_social_facebook = models.URLField(blank=True, null=True)
    red_social_x = models.URLField(blank=True, null=True)
    campo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Alquiler(models.Model):
    idalquiler = models.AutoField(primary_key=True)
    fechalquiler = models.DateField()
    hora_inicio_reserva = models.TimeField()
    horafinplanificada = models.TimeField()
    horafinrealreserva = models.TimeField(blank=True, null=True)
    costo_alquiler = models.DecimalField(max_digits=10, decimal_places=2)
    calificacioncliente = models.IntegerField(blank=True, null=True)
    calificacionnegocio = models.IntegerField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    idcliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idevento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    estado_alquiler = models.CharField(
        max_length=20,
        choices=[("Activo", "Activo"), ("Cancelado", "Cancelado"), ("Finalizado", "Finalizado")]
    )

    def __str__(self):
        return f"Alquiler {self.idalquiler} - Cliente: {self.idcliente}"


class Servicio(models.Model):
    idservicio = models.AutoField(primary_key=True)
    descripcionservicio = models.CharField(max_length=200)
    valorporunidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descripcionservicio


class AlquilerServicio(models.Model):
    idalquiler_servicio = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    idalquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)
    idservicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio {self.idservicio} para Alquiler {self.idalquiler}"


class Promocion(models.Model):
    idpromocion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    idalquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)

    def __str__(self):
        return f"Promocion {self.descripcion} ({self.porcentaje_descuento}%)"


class Eventualidad(models.Model):
    ideventualidad = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    fecha_eventualidad = models.DateField()
    idalquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)

    def __str__(self):
        return f"Eventualidad {self.ideventualidad} - {self.descripcion}"


class FotoEvento(models.Model):
    idfoto_evento = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to="eventos/imagenes/")
    idevento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Foto de Evento {self.idevento}"


class FotoServicio(models.Model):
    idfoto_servicio = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to="servicios/imagenes/")
    idservicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Foto de Servicio {self.idservicio}"
