from django.shortcuts import render
from negocio.models import TipoEvento
# Create your views here.
def home_view(request):
    tipoEventos = TipoEvento.objects.all()[:3]
    return render(request, 'main/home.html', {"tipoEventos": tipoEventos})