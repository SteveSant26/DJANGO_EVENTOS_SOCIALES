# negocio/urls.py
from django.urls import path
from .views import servicios

urlpatterns = [
    path('', servicios.index, name='index'),
    path('about-us/', servicios.about_us, name='about_us'),
    path('blog-post/', servicios.blog_post, name='blog_post'),
    path('blog/', servicios.blog, name='blog'),
    path('contact-us/', servicios.contact_us, name='contact_us'),
    path('full-width/', servicios.full_width, name='full_width'),
    path('portfolio-item/', servicios.portfolio_item, name='portfolio_item'),
    path('portfolio/', servicios.portfolio, name='portfolio'),
    path('services/', servicios.services, name='services'),
    path('eventos/', servicios.lista_eventos, name='lista_eventos'),
]


