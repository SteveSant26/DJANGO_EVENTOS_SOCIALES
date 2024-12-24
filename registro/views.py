from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


from .forms import SignUpForm, LoginForm


def signup_view(request):
    if request.user.is_authenticated:
        messages.error(request, "Ya estás autenticado/a.")
        return redirect("clientes:profile")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            messages.success(
                request,
                "Cuenta creada con éxito. Por favor, verifica tu correo electrónico.",
            )
            return redirect("clientes:profile")
        else:
            messages.error(
                request,
                "Hubo errores en el formulario. Por favor, corrígelos e intenta nuevamente.",
            )
    else:
        form = SignUpForm()

    return render(request, "registro/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, "Ya estás autenticado/a.")
        return redirect("clientes:profile")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Bienvenido/a, {user.username}!")
            return redirect("main:home")
        else:
            messages.error(request, form.error_messages)

    else:
        form = LoginForm()

    return render(request, "registro/login.html", {"form": form})


@login_required
def logout_view(request):
    messages.success(request, "¡Hasta luego!")
    logout(request)
    return redirect("main:home")
