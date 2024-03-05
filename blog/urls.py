""" URLs de la app "app_grupo_alvi", la cual es la app que usarán los clientes.

Voy también a agregar la URL a la API para poder obtener el Subtotal de multiplicar el Precio de un Producto por su
respectiva Cantidad de los Formsets con los menús desplegables de los productos. Los formularios de Cotizaciones, y
posiblemente los de Pedidos y de Órdenes de Compra, van a entrar a esta URL para usar la API, y luego te darán como
output (como resultado) el resultado de multiplicar el número de "Cantidad" por el precio de venta de ese Producto.
Y todo de manera instantánea en el front-end, sin la necesidad de refrescar la página.

The URL for the view that gets the product of a "Pedido" from its respective "Cotización" includes a dynamic segment
(<int:cotizacion_id>/) that will capture the order id from the URL and pass it to the view.
"""


from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),    # Página de inicio

    # Términos y Condiciones
    path('terms-and-conditions-no-usar', views.terms_and_conditions, name='terms_and_conditions'),

    # # Política de Privacidad
    # path('politica-de-privacidad', views.politica_de_privacidad, name='politica_de_privacidad'),


    # # Formulario para Iniciar Sesión
    # path('iniciar-sesion', views.iniciar_sesion, name='iniciar_sesion'),
    #
    # # Página para Cerrar Sesión
    # path('cerrar-sesion', views.cerrar_sesion, name='cerrar_sesion'),




]