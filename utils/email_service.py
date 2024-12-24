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
        subject = "Código de Verificación"
        message = (
            f"Hola {perfil.cliente.username},\n\n"
            f"Gracias por registrarte en nuestra plataforma. Tu código de verificación es: {perfil.codigo_verificacion}\n\n"
            "Por favor, utiliza este código para verificar tu cuenta. Si tienes alguna pregunta, no dudes en contactarnos.\n\n"
            "Saludos cordiales,\n"
            "El equipo de soporte"
        )
        recipient_list = [perfil.correo]

        EmailService.enviar_email(subject, message, recipient_list)

    @staticmethod
    def enviar_codigo_reserva(reserva: ReservaEvento):
        subject = "Confirmación de Reserva"
        message = (
            f"Estimado/a {reserva.cliente},\n\n"
            f"Gracias por realizar una reserva para el evento \"{reserva.evento}\".\n\n"
            "Por favor, utiliza el siguiente código para confirmar tu reserva:\n\n"
            f"Código de confirmación: {reserva.codigo_confirmacion_reserva}\n\n"
            "Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en contactarnos.\n\n"
            "Saludos cordiales,\n"
            "El equipo de Gestión de Alquileres"
        )
        recipient_list = [reserva.cliente.email]

        EmailService.enviar_email(subject, message, recipient_list)
