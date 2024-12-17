# negocio/views.py
from django.shortcuts import render
from .models import Evento

# Vista para la página de inicio

def about_us(request):
    return render(request, 'negocio/about-us.html')

def blog_post(request):
    return render(request, 'negocio/blog-post.html')

def blog(request):
    return render(request, 'negocio/blog.html')

def contact_us(request):
    return render(request, 'negocio/contact-us.html')

def full_width(request):
    return render(request, 'negocio/full-width.html')

def index(request):
    return render(request, 'negocio/index.html')

def portfolio_item(request):
    return render(request, 'negocio/portfolio-item.html')

def portfolio(request):
    return render(request, 'negocio/portfolio.html')

def services(request):
    return render(request, 'negocio/services.html')


def lista_eventos(request):
    eventos = Evento.objects.all()  # Traer todos los eventos desde la base de datos
    return render(request, 'negocio/lista_eventos.html', {'eventos': eventos})

