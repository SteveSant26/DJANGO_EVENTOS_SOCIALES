from django.urls import path
from . import views as vistas

app_name = 'clientes'

urlpatterns = [
    path("registro/", vistas.crear_cliente, name="registro"),
    path("login/", vistas.login, name="login"),
    path("mis-datos/", vistas.actualizar_cliente, name="mis_datos"),
]