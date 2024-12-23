from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("verificar-correo/", views.verificar_correo, name="verificar_correo"),
    path("reenviar-correo/", views.reenvio_correo_validacion, name="reenvio_correo"),
]
