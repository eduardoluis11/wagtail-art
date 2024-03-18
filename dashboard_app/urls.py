""" URLS.py for the dashboard_app app.

"""

from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),    # Página de inicio

    # Page for Registering a New Artwork Page
    path('register-artwork', views.register_artwork, name='register_artwork'),

]
