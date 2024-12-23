from django.urls import path
from . import views


app_name = "reservas"



urlpatterns = [
    path("", views.reservas_view, name="listar_reservas"),
    path("<int:id>/", views.reserva_detail, name="reserva_detail"),
    path("create/<int:evento_id>/", views.reserva_new, name="reserva_new"),
    path("<int:id>/servicios/", views.servicios_reserva, name="servicios_reserva"),
    path("<int:id>/confirmar/", views.confirmar_reserva, name="confirmar_reserva"),
]
