from django.core.mail import send_mail
from django.conf import settings

from clientes.models import InformacionCliente
from reservas.models import ReservaEvento


class EmailService:

    @staticmethod
    def enviar_email(subject, message, recipient_list):

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    @staticmethod
    def enviar_codigo_verificacion(perfil: InformacionCliente):
        codigo = perfil.generar_codigo_verificacion()
        subject = "Código de verificación"
        message = (
            f"Hola {perfil.cliente.username},\n\n"
            f"Gracias por registrarte. Tu código de verificación es: {codigo}\n\n"
            "Por favor, utiliza este código para verificar tu cuenta."
        )
        recipient_list = [perfil.correo]

        EmailService.enviar_email(subject, message, recipient_list)

    @staticmethod
    def enviar_codigo_reserva(reserva: ReservaEvento):

        
        codigo_confirmacion = reserva.crear_codigo_confirmacion()
        reserva.save()

        asunto = "Confirmación de Alquiler"
        mensaje = f"""
        Estimado/a {reserva.cliente},
        
        Gracias por realizar su reserva para el evento "{reserva.evento}".
        Por favor, use el siguiente código para confirmar su reserva:
        
        Código de confirmación: {codigo_confirmacion}
        
        Saludos,
        Equipo de Gestión de Alquileres
        """
        destinatarios = [reserva.cliente.email]

        EmailService.send_email(asunto, mensaje, destinatarios)
