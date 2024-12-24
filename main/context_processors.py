from configuracion.models import Negocio

def settings_context(request):
    return {'configuracion': Negocio.objects.get_or_create()}

