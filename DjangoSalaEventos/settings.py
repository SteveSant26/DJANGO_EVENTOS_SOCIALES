from pathlib import Path
import environ
import cloudinary
import cloudinary.uploader
import cloudinary.api
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
entorno = environ.Env()
entorno.read_env()  # Reads from .env file

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = entorno("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = entorno("DEBUG", default=False)

ALLOWED_HOSTS = entorno.list("ALLOWED_HOSTS", default=[])

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "crispy_forms",
    "crispy_bootstrap5",
    "cloudinary",
    "cloudinary_storage",
    "django_filters",
    "import_export",
    # Custom apps
    "negocio",
    "registro",
    "clientes",
    "main",
    "reservas",
    "configuracion",
]


JAZZMIN_SETTINGS = {
    "site_title": "Django Sala de Eventos",
    "site_header": "Django Sala de Eventos",
    "site_brand": "Django Sala de Eventos",
    "site_logo": None,
    "welcome_sign": "Bienvenido al panel de administración de Django Sala de Eventos",
    "search_model": "auth.User",
    "topmenu_links": [
        {"name": "Inicio", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Home", "url": "main:home", "permissions": ["auth.view_user"]},
        {"name": "Salir", "url": "admin:logout", "permissions": ["auth.view_user"]},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [
        "sessions",
    ],
    "hide_models": [
        "auth.Permission",
        "auth.Group",
    ],
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-success navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "cyborg",
    "dark_mode_theme": "solar",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}


CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DjangoSalaEventos.urls"

# Templates settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.context_processors.settings_context",
            ],
        },
    },
]

WSGI_APPLICATION = "DjangoSalaEventos.wsgi.application"

# Cloudinary configuration
cloudinary.config(
    cloud_name=entorno("CLOUDINARY_CLOUD_NAME"),
    api_key=entorno("CLOUDINARY_API_KEY"),
    api_secret=entorno("CLOUDINARY_API_SECRET"),
)
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = entorno("EMAIL_HOST")
EMAIL_PORT = entorno("EMAIL_PORT")
EMAIL_USE_TLS = entorno("EMAIL_USE_TLS")
EMAIL_HOST_USER = entorno("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = entorno("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = entorno("DEFAULT_FROM_EMAIL")

# Database settings
DATABASES = {
    "default": dj_database_url.parse(entorno("DATABASE_URL"))
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization settings
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Archivos de medios
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login URLs
LOGIN_URL = "registro:login"
LOGIN_REDIRECT_URL = "main:home"
LOGOUT_REDIRECT_URL = "registro:login"


if not DEBUG:

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
