from django.contrib import admin
from django.urls import path, include








urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path('', include('negocio.urls')),  # Aquí se incluyen las URLs de negocio
]
