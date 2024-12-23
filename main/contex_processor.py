from django.conf import settings
from configuracion.models import Negocio

def settings_context(request):
    return {'configuracion': Negocio.objects.first()}

