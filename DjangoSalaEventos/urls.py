from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("negocio/", include("negocio.urls")),
    path("clientes/", include("clientes.urls")),
    path("reservas/", include("reservas.urls")),
]
