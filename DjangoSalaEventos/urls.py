
from django.contrib import admin
from django.urls import path, include



admin.site.site_header = "Administración de Sala de Eventos"
admin.site.site_title = "Administración de Sala de Eventos"
admin.site.index_title = "Bienvenido a la administración de la Sala de Eventos"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('negocio.urls')),  # Aquí se incluyen las URLs de negocio
]
