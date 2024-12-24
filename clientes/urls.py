from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [

    path("profile/", views.profile_view, name="profile"),
    path("verificar-correo/", views.verificar_correo, name="verificar_correo"),
    path("reenviar-correo/", views.reenvio_correo_validacion, name="reenvio_correo"),
]
