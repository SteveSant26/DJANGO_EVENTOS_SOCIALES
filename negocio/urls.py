# negocio/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about_us'),
    path('blog-post/', views.blog_post, name='blog_post'),
    path('blog/', views.blog, name='blog'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('full-width/', views.full_width, name='full_width'),
    path('portfolio-item/', views.portfolio_item, name='portfolio_item'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('services/', views.services, name='services'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
]


