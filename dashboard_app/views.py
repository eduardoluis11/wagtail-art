from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# This imports my forms from forms.py
from .forms import AddArtworkForm, AddProductForm

# This imports the models
from .models import ArtworkPage

# Create your views here.

""" View for Registering a New Product.

"""


def register_product(request):

    main_form = AddProductForm()  # Form for Registering Products

    # # Formset para registrar una o varias Imágenes Secundarias
    # formset_imagenes_secundarias = FormsetImagenesSecundariasParaUnProducto()

    # # Lista vacía para meter las imágenes secundarias validadas
    # lista_de_imagenes_secundarias_validadas = []

    # If the User Submits the Form
    if request.method == "POST":

        pass
    #
    #     # This overwrites the main_form form with the sanitized data that the user submitted
    #     main_form = AddArtworkForm(request.POST, request.FILES)
    #
    #     # # formset_imagenes_secundarias = FormsetImagenesSecundariasParaUnProducto(request.POST, request.FILES)
    #
    #     # if formulario_registrar_productos.is_valid() and formset_imagenes_secundarias.is_valid():
    #
    #     # This validates the forms. If any of the forms is invalid, NOTHING WILL BE Inserted Into TO THE DATABASE
    #     if main_form.is_valid():
    #
    #         # This gets the sanitized data from the form
    #         data = main_form.cleaned_data
    #
    #         # This gets the sanitized data from the form
    #         date = data["date"]
    #         intro = data["intro"]
    #         image = data["image"]
    #         prompt = data["prompt"]
    #         has_copyright = data["copyright"]
    #         explanation = data["explanation"]
    #         ai_used = data["ai_used"]
    #         specify_ai_if_other = data["specify_ai_if_other"]
    #
    #         # This will insert the data into the Artwork Page model
    #         new_artwork_page = ArtworkPage(date=date, intro=intro, image=image, prompt=prompt, copyright=has_copyright,
    #                                        explanation=explanation, ai_used=ai_used,
    #                                        specify_ai_if_other=specify_ai_if_other
    #                                        )
    #         new_artwork_page.save()     # End of the snippet that creates a new Artwork Page
    #
    #         # Confirmation flash message
    #         messages.success(request, "The Artwork has been registered successfully.")
    #
    #         # This redirects the user to the Artwork Page
    #         return render(request, 'dashboard_app/register-artwork.html', {
    #             "main_form": main_form,
    #         })


            #     # Esto agarra todos los campos ya validados/sanitizados de los formularios
            #     datos_validados_formulario_productos = formulario_registrar_productos.cleaned_data
            #     datos_validados_formset_imagenes_secundarias = formset_imagenes_secundarias.cleaned_data
            #
            #     # Campos del formulario de Registrar Productos rellenados por el usuario que ya han sido validados
            #     nombre_del_producto = datos_validados_formulario_productos["nombre_del_producto"]
            #     clave_sku = datos_validados_formulario_productos["clave_sku"]
            #     descripcion = datos_validados_formulario_productos["descripcion"]
            #     unidad_de_medida = datos_validados_formulario_productos["unidad_de_medida"]
            #     categoria = datos_validados_formulario_productos["categoria"]
            #     precio_de_lista = datos_validados_formulario_productos["precio_de_lista"]
            #     precio_de_venta = datos_validados_formulario_productos["precio_de_venta"]
            #     proveedor = datos_validados_formulario_productos["proveedor"]
            #     precio_de_compra = datos_validados_formulario_productos["precio_de_compra"]
            #     imagen_principal = datos_validados_formulario_productos["imagen_principal"]
            #     # imagen_secundaria = datos_validados["imagen_secundaria"]
            #     ficha_tecnica = datos_validados_formulario_productos["ficha_tecnica"]
            #
            #     # BUG: esto me está generando un bug de Django
            #     # # Campo del formset de Imagenes Secundarias de un producto.
            #     # imagen_secundaria = datos_validados_formset_imagenes_secundarias["imagen_secundaria"]
            #
            #     # Voy a meter los datos del Producto en los modelos del Producto y de sus Imagenes Secundarias
            #
            #     # Fecha y hora actual (timestamp)
            #     timestamp = datetime.datetime.now()
            #
            #     try:
            #         # Check if a product with the same SKU already exists
            #         Producto.objects.get(clave_sku=clave_sku)
            #
            #         # If the above line does not raise an ObjectDoesNotExist exception,
            #         # it means a product with the same SKU already exists. And since clave_sku is a unique field,
            #         # we can display a flash error message to the user in the front-end, without showing Django error
            #         # messages.
            #         messages.error(request, 'Ya existe in producto con esta clave SKU. Por favor, usa otra clave '
            #                                 'SKU.')
            #
            #         # Esto renderiza el Formulario de Registrar un Producto
            #         return render(request, 'productos/registrar-productos.html', {
            #             "formulario_registrar_productos": formulario_registrar_productos,
            #             "formset_imagenes_secundarias": formset_imagenes_secundarias,
            #             # "usuario_es_capturista": usuario_es_capturista,
            #         })
            #
            #     # Si la clave SKU escrita por el usuario no existe en la base de datos, se creará un nuevo producto
            #     except ObjectDoesNotExist:
            #
            #         # Query Set que prepara los datos para meterlos en le modelo de Producto
            #         nuevo_producto = Producto(nombre_del_producto=nombre_del_producto, clave_sku=clave_sku,
            #                                   descripcion=descripcion, unidad_de_medida=unidad_de_medida, categoria=categoria,
            #                                   precio_de_lista=precio_de_lista,
            #                                   # precio_de_compra=precio_de_compra,
            #                                   precio_de_venta=precio_de_venta,
            #                                   imagen_principal=imagen_principal, ficha_tecnica=ficha_tecnica)
            #
            #         # Esto mete al nuevo producto en la base de datos. Debo hacerlo antes de asignarle las imágenes secundarias
            #         nuevo_producto.save()
            #
            #         # Si el Proveedor y/o el Precio de Compra no están vacíos, los meteré en el modelo de Productos de
            #         # Proveedores.
            #         if proveedor is not None or precio_de_compra is not None:
            #             # Query Set que prepara los datos para meterlos en el modelo de Producto
            #             nuevo_precio_de_compra_del_proveedor = PrecioDeCompraDelProveedor(proveedor=proveedor,
            #                                                                               precio_de_compra=precio_de_compra,
            #                                                                               producto=nuevo_producto)
            #
            #             # Esto mete el nuevo Producto de este Proveedor en la base de datos
            #             nuevo_precio_de_compra_del_proveedor.save()
            #
            #         # Imágenes Secundarias
            #         # Esto mete las imágenes en la Lista de Python de imágenes secundarias
            #         for imagen in formset_imagenes_secundarias:
            #
            #             # Esto agarra las Imagenes Secundarias subidas por el usuario del Formulario
            #             # Uso get() para evitar un bug y así hacer opcional el campo "Imagen Secundaria"
            #             if imagen.cleaned_data.get('imagen_secundaria') is not None:
            #                 datos_validados_imagen_secundaria = imagen.cleaned_data['imagen_secundaria']
            #
            #                 # Agrega la imagen a la Lista de Python
            #                 lista_de_imagenes_secundarias_validadas.append(datos_validados_imagen_secundaria)
            #
            #         # Ahora, si hay mínimo una imagen secundaria en la Lista de Python, las meteré en su respectivo modelo
            #         if lista_de_imagenes_secundarias_validadas is not None:
            #
            #             # Esto mete cada imagen de la lista en el modelo de Imágenes Secundarias
            #             for imagen in lista_de_imagenes_secundarias_validadas:
            #
            #                 # Debo meter la imagen con su respectivo Producto
            #                 nueva_imagen = ImagenSecundariaDeUnProducto(
            #                     imagen_secundaria=imagen, producto=nuevo_producto)
            #
            #                 # Esto termine de meter el nuevo documento al modelo de Otros Documentos
            #                 nueva_imagen.save()
            #
            #                 # Fin de haber metido todas las imágenes secundarias en el modelo de Imagenes Secundarias
            #
            #         # Mensaje flash de confirmacion de que se metió el Producto y las Imagenes a la base de datos
            #         messages.success(request, "Se ha registrado correctamente el producto.")
            #
            #         # Esto redirige al usuario a la lista de Productos
            #         return HttpResponseRedirect(reverse("lista_de_productos"))
            #
            #         # return render(request, "iniciar-sesion.html", {
            #         #     "formulario_registrar_productos": formulario_registrar_productos,
            #         #     "formset_imagenes_secundarias": formset_imagenes_secundarias,
            #         # })

        # # If the form is invalid (if the user writes malicious code), it will display the error message to the user
        # else:
        #
        #     # Flash error message for the front-end
        #
        #     # Error message if the main form is filled out incorrectly
        #     messages.error(request, main_form.errors)
        #
        #     # Esto renderiza el Formulario de Registrar un Producto
        #     return render(request, 'dashboard_app/products/register-product.html', {
        #         "main_form": main_form,
        #     })

    # Esto renderiza el formulario si el usuario entró a la página sin enviar el formulario
    else:
        # Esto renderiza el Formulario de Registrar un Producto
        return render(request, 'dashboard_app/products/register-product.html', {
            "main_form": main_form,
            # "formulario_registrar_productos": formulario_registrar_productos,
        })



""" Front-end Form for registering a New Artwork made with Stable Diffusion.

I WON'T end up using this view, since inserting an image from here would be too complicated, and since the Wagtail
Admin Panel does a WAY better job in inserting this, anyways.
"""


def register_artwork(request):

    pass

#     main_form = AddArtworkForm()  # Form for Registering Artwork Pages
#
#     # # Formset para registrar una o varias Imágenes Secundarias
#     # formset_imagenes_secundarias = FormsetImagenesSecundariasParaUnProducto()
#
#     # # Lista vacía para meter las imágenes secundarias validadas
#     # lista_de_imagenes_secundarias_validadas = []
#
#     # If the User Submits the Form
#     if request.method == "POST":
#
#         # pass
#
#         # This overwrites the main_form form with the sanitized data that the user submitted
#         main_form = AddArtworkForm(request.POST, request.FILES)
#
#         # # formset_imagenes_secundarias = FormsetImagenesSecundariasParaUnProducto(request.POST, request.FILES)
#
#         # if formulario_registrar_productos.is_valid() and formset_imagenes_secundarias.is_valid():
#
#         # This validates the forms. If any of the forms is invalid, NOTHING WILL BE Inserted Into TO THE DATABASE
#         if main_form.is_valid():
#
#             # This gets the sanitized data from the form
#             data = main_form.cleaned_data
#
#             # This gets the sanitized data from the form
#             date = data["date"]
#             intro = data["intro"]
#             image = data["image"]
#             prompt = data["prompt"]
#             has_copyright = data["copyright"]
#             explanation = data["explanation"]
#             ai_used = data["ai_used"]
#             specify_ai_if_other = data["specify_ai_if_other"]
#
#             # This will insert the data into the Artwork Page model
#             new_artwork_page = ArtworkPage(date=date, intro=intro, image=image, prompt=prompt, copyright=has_copyright,
#                                            explanation=explanation, ai_used=ai_used,
#                                            specify_ai_if_other=specify_ai_if_other
#                                            )
#             new_artwork_page.save()     # End of the snippet that creates a new Artwork Page
#
#             # Confirmation flash message
#             messages.success(request, "The Artwork has been registered successfully.")
#
#             # This redirects the user to the Artwork Page
#             return render(request, 'dashboard_app/register-artwork.html', {
#                 "main_form": main_form,
#             })
#
#
#             #     # Esto agarra todos los campos ya validados/sanitizados de los formularios
#             #     datos_validados_formulario_productos = formulario_registrar_productos.cleaned_data
#             #     datos_validados_formset_imagenes_secundarias = formset_imagenes_secundarias.cleaned_data
#             #
#             #     # Campos del formulario de Registrar Productos rellenados por el usuario que ya han sido validados
#             #     nombre_del_producto = datos_validados_formulario_productos["nombre_del_producto"]
#             #     clave_sku = datos_validados_formulario_productos["clave_sku"]
#             #     descripcion = datos_validados_formulario_productos["descripcion"]
#             #     unidad_de_medida = datos_validados_formulario_productos["unidad_de_medida"]
#             #     categoria = datos_validados_formulario_productos["categoria"]
#             #     precio_de_lista = datos_validados_formulario_productos["precio_de_lista"]
#             #     precio_de_venta = datos_validados_formulario_productos["precio_de_venta"]
#             #     proveedor = datos_validados_formulario_productos["proveedor"]
#             #     precio_de_compra = datos_validados_formulario_productos["precio_de_compra"]
#             #     imagen_principal = datos_validados_formulario_productos["imagen_principal"]
#             #     # imagen_secundaria = datos_validados["imagen_secundaria"]
#             #     ficha_tecnica = datos_validados_formulario_productos["ficha_tecnica"]
#             #
#             #     # BUG: esto me está generando un bug de Django
#             #     # # Campo del formset de Imagenes Secundarias de un producto.
#             #     # imagen_secundaria = datos_validados_formset_imagenes_secundarias["imagen_secundaria"]
#             #
#             #     # Voy a meter los datos del Producto en los modelos del Producto y de sus Imagenes Secundarias
#             #
#             #     # Fecha y hora actual (timestamp)
#             #     timestamp = datetime.datetime.now()
#             #
#             #     try:
#             #         # Check if a product with the same SKU already exists
#             #         Producto.objects.get(clave_sku=clave_sku)
#             #
#             #         # If the above line does not raise an ObjectDoesNotExist exception,
#             #         # it means a product with the same SKU already exists. And since clave_sku is a unique field,
#             #         # we can display a flash error message to the user in the front-end, without showing Django error
#             #         # messages.
#             #         messages.error(request, 'Ya existe in producto con esta clave SKU. Por favor, usa otra clave '
#             #                                 'SKU.')
#             #
#             #         # Esto renderiza el Formulario de Registrar un Producto
#             #         return render(request, 'productos/registrar-productos.html', {
#             #             "formulario_registrar_productos": formulario_registrar_productos,
#             #             "formset_imagenes_secundarias": formset_imagenes_secundarias,
#             #             # "usuario_es_capturista": usuario_es_capturista,
#             #         })
#             #
#             #     # Si la clave SKU escrita por el usuario no existe en la base de datos, se creará un nuevo producto
#             #     except ObjectDoesNotExist:
#             #
#             #         # Query Set que prepara los datos para meterlos en le modelo de Producto
#             #         nuevo_producto = Producto(nombre_del_producto=nombre_del_producto, clave_sku=clave_sku,
#             #                                   descripcion=descripcion, unidad_de_medida=unidad_de_medida, categoria=categoria,
#             #                                   precio_de_lista=precio_de_lista,
#             #                                   # precio_de_compra=precio_de_compra,
#             #                                   precio_de_venta=precio_de_venta,
#             #                                   imagen_principal=imagen_principal, ficha_tecnica=ficha_tecnica)
#             #
#             #         # Esto mete al nuevo producto en la base de datos. Debo hacerlo antes de asignarle las imágenes secundarias
#             #         nuevo_producto.save()
#             #
#             #         # Si el Proveedor y/o el Precio de Compra no están vacíos, los meteré en el modelo de Productos de
#             #         # Proveedores.
#             #         if proveedor is not None or precio_de_compra is not None:
#             #             # Query Set que prepara los datos para meterlos en el modelo de Producto
#             #             nuevo_precio_de_compra_del_proveedor = PrecioDeCompraDelProveedor(proveedor=proveedor,
#             #                                                                               precio_de_compra=precio_de_compra,
#             #                                                                               producto=nuevo_producto)
#             #
#             #             # Esto mete el nuevo Producto de este Proveedor en la base de datos
#             #             nuevo_precio_de_compra_del_proveedor.save()
#             #
#             #         # Imágenes Secundarias
#             #         # Esto mete las imágenes en la Lista de Python de imágenes secundarias
#             #         for imagen in formset_imagenes_secundarias:
#             #
#             #             # Esto agarra las Imagenes Secundarias subidas por el usuario del Formulario
#             #             # Uso get() para evitar un bug y así hacer opcional el campo "Imagen Secundaria"
#             #             if imagen.cleaned_data.get('imagen_secundaria') is not None:
#             #                 datos_validados_imagen_secundaria = imagen.cleaned_data['imagen_secundaria']
#             #
#             #                 # Agrega la imagen a la Lista de Python
#             #                 lista_de_imagenes_secundarias_validadas.append(datos_validados_imagen_secundaria)
#             #
#             #         # Ahora, si hay mínimo una imagen secundaria en la Lista de Python, las meteré en su respectivo modelo
#             #         if lista_de_imagenes_secundarias_validadas is not None:
#             #
#             #             # Esto mete cada imagen de la lista en el modelo de Imágenes Secundarias
#             #             for imagen in lista_de_imagenes_secundarias_validadas:
#             #
#             #                 # Debo meter la imagen con su respectivo Producto
#             #                 nueva_imagen = ImagenSecundariaDeUnProducto(
#             #                     imagen_secundaria=imagen, producto=nuevo_producto)
#             #
#             #                 # Esto termine de meter el nuevo documento al modelo de Otros Documentos
#             #                 nueva_imagen.save()
#             #
#             #                 # Fin de haber metido todas las imágenes secundarias en el modelo de Imagenes Secundarias
#             #
#             #         # Mensaje flash de confirmacion de que se metió el Producto y las Imagenes a la base de datos
#             #         messages.success(request, "Se ha registrado correctamente el producto.")
#             #
#             #         # Esto redirige al usuario a la lista de Productos
#             #         return HttpResponseRedirect(reverse("lista_de_productos"))
#             #
#             #         # return render(request, "iniciar-sesion.html", {
#             #         #     "formulario_registrar_productos": formulario_registrar_productos,
#             #         #     "formset_imagenes_secundarias": formset_imagenes_secundarias,
#             #         # })
#
#         # If the form is invalid (if the user writes malicious code), it will display the error message to the user
#         else:
#
#             # Flash error message for the front-end
#
#             # Error message if the main form is filled out incorrectly
#             messages.error(request, main_form.errors)
#
#             # Esto renderiza el Formulario de Registrar un Producto
#             return render(request, 'dashboard_app/register-artwork.html', {
#                 "main_form": main_form,
#             })
#
#     # Esto renderiza el formulario si el usuario entró a la página sin enviar el formulario
#     else:
#         # Esto renderiza el Formulario de Registrar un Producto
#         return render(request, 'dashboard_app/register-artwork.html', {
#             "main_form": main_form,
#             # "formulario_registrar_productos": formulario_registrar_productos,
#         })

