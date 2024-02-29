from .base import *

# Aquí se guarda la clave de Django en el archivo .env, es decir, en las
# variables de entorno (fuente: https://codinggear.blog/django-environment-variables/)
from dotenv import load_dotenv
import os

# Esto me corrige un bug que dice que "Necesitaba Autenticación para poder Enviar un Email"
import django.core.mail.backends.smtp


load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
