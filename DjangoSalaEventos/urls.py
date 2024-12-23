from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path('', include('negocio.urls')),  
    path('clientes/', include('clientes.urls')),
]
