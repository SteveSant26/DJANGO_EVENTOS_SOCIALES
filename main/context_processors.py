from django.conf import settings
from configuracion.models import Negocio

def settings_context(request):

    print(Negocio.objects.exists())
    print(Negocio.objects.first())
    return {'configuracion': Negocio.objects.first()}

