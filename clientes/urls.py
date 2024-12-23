from django.urls import path
from . import views as vistas

app_name = "clientes"

urlpatterns = [
    path("signup/", vistas.signup_view, name="signup"),
    path("login/", vistas.login_view, name="login"),
    path("logout/", vistas.logout_view, name="logout"),
    path("profile/", vistas.profile_view, name="profile"),
    path("verificar-correo/", vistas.verificar_correo, name="verificar_correo"),
    path("reenviar-correo/", vistas.reenvio_correo_validacion, name="reenvio_correo"),
]
