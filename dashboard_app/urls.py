"""URLS.py for the dashboard_app app."""

from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),    # Página de inicio
    # Page for Registering a New Artwork Page
    path("register-product", views.register_product, name="register_product"),
    # Page for Registering a New Artwork Page. DO NOT PUT A TRAILING SLASH.
    path("register-artwork", views.register_artwork, name="register_artwork"),
]
