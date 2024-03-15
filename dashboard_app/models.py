from django.db import models

# Create your models here.

# """ ### Product Model
#
# All the basic data for each product will be stored in this model.
#
# Then, in the model called "Products of an Order," I will call the FK with the product selected by the user and add as
# additional fields the selected quantity (for example, "3" if they want to buy 3 containers) and the order to which
# that quantity of products belongs (as a FK). I could also include the subtotal. But for now, the only thing I need
# in the Product Model of a Purchase Order is the quantity of products ordered in a purchase order.
#
# #### Fields:
# - Product Name*
# - Unit Price. (THIS DOES NOT GO HERE, and it is REDUNDANT. I already have about 3 prices here).
# - SKU (Stock Keeping Unit)* (40 characters).
# - Description* (text) (500 characters).
# - Unit of Measurement* (Piece, service, box) -> I'll send you the catalog.
# - Category* -> CRUD. Apparently, the user can write whatever they want here. I'll put it as Varchar, 100 characters.
# - List Price* (100 EUR) (I think "EUR" stands for "euros") (14 digits with 2 decimals).
# - Purchase Price* (percentage defined by supplier but modifiable) (one to many) (FK).
# - Sale Price* (same as list) 100 EUR. There is no difference between this and the "List Price." They must be exactly
# the same price. In the future, this field will be modified to make them different.
# - Main Image* PNG. (ImageField).
# - Technical Sheet (File). (FileField).
#
# * Secondary Images: I will create a new model to assign multiple secondary images to each product, as a product can
# have several secondary images.
#
# There is only one supplier that offers a volume discount. The rest have a price per product. Normally it's 28% - 10% (35.2%).
#
# I think of creating a model called "Supplier Purchase Prices," and I will take the records from that model as FK in the
# "Purchase Price" field in the Product model. That model I will create will have only and exclusively the purchase prices from
# the suppliers. I don't think it will be a percentage, but rather a normal price, only that the discount from that specific
# supplier is already applied to it.
#
# The SKU field must be unique for each product. There cannot be 2 products with the same SKU. Therefore, I put a restriction
# on it with the "unique" keyword.
#
# To prevent any confusions, I will call "Product From the Supplier" to the "Supllier Purchase Prices" model. In reality,
# that's what that model is: it stores the products offered by that supplier.
# """
#
#
# class Product(models.Model):
#     product_name = models.CharField(max_length=200)  # Product Name
#
#     sku_code = models.CharField(max_length=40, unique=True)  # SKU (Stock Keeping Unit) Code
#     description = models.CharField(max_length=500)  # Description
#     unit_of_measurement = models.CharField(max_length=20)  # Unit of Measurement
#     category = models.CharField(max_length=100)    # Category
#     list_price = models.DecimalField(max_digits=14, decimal_places=2)  # List Price
#
#     # Purchase Price (defined by supplier but modifiable)
#     purchase_price = models.ForeignKey('ProductFromTheSupplier', on_delete=models.CASCADE)
#
#     # Sale Price (same as list price, initially)
#     sale_price = models.DecimalField(max_digits=14, decimal_places=2)  # Sale Price
#
#     main_image = models.ImageField(upload_to='products/main-images')    # Main Image
#
#     # Technical Sheet (Optional)
#     technical_sheet = models.FileField(upload_to='products/technical-sheets', blank=True, null=True)
#
#     # This displays the Product's name and SKU code
#     def __str__(self):
#         return f"{self.product_name} - SKU: {self.sku_code}"
#
#
#
# """ Modelo con los Precios de Compra de los Proveedores.
#
# Dado a que un producto del modelo de Productos puede tener uno o varios precios de compra, tengo que crear este modelo.
# Así aquí puedo almacenar todos los precios de compra como registros en este modelo, y se le pueden asignar varios
# precios de compra a un solo producto usando una FK de este model en el modelo de Productos.
#
# Dado a que cada proveedor define su propio precio de compra, creo que pondré otro campo llamado "proveedor". Ese campo
# debería ser una FK del modelo de Proveedores.
#
# *Campos:
# - Precio de Compra (14 dígitos con 2 decimales).
# - Proveedor (FK).
# - Producto (FK)
#
# El "locale" y el "format_string" va a imprimirme el precio en pesos mexicanos, en donde se mostraran los decimales con
# comas en el panel de admin de Django y cuando se imprima el precio de compra como Foreign Key. Así se debe hacer en
# español.
#
# Por motivos de user experience, le cambiare el Meta del modelo “Precios de Compra de los Proveedores” a “Productos de
# los Proveedores”. Eso es para evitar confusiones.
#
# Solo haré que el producto sea obligatorio. TANTO EL PRECIO DE COMPRA COMO EL PROVEEDOR DEBEN SER OPCIONALES.
# """
#
#
# class ProductFromTheSupplier(models.Model):
#
#     # Proveedor que ofrece este precio
#     proveedor = models.ForeignKey("Supplier", on_delete=models.CASCADE, related_name="proveedor_de_este_precio",
#                                   null=True, blank=True)
#
#     # Producto (FK)
#     producto = models.ForeignKey("Product", on_delete=models.CASCADE,
#                                  related_name="producto_que_tiene_este_precio_de_compra")
#
#     # Precio de Compra
#     precio_de_compra = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Precio de compra ($)",
#                                            null=True, blank=True, default=0)
#
#     # Nombre en plural arreglado en el Panel de Admin de Django
#     class Meta:
#         verbose_name_plural = "Productos de los Proveedores"
#
#     # Esto muestra el precio de compra, junto con el nombre del proveedor.
#     def __str__(self):
#         return (f"{self.producto.product_name} - {self.proveedor} - "
#                 f"${self.precio_de_compra}")
#
#
# """ Modelo de Proveedores.
#
# * Campos:
# - Nombre del Proveedor (Alias) (ej: Umbrella).  X
# - Razón social (ej: Umbrella Corp). X
# - RFC (y Datos Fiscales (PREGUNTAR QUE ES ESTO DE DATOS FISCALES)) (ej: XAXX010101000) (13 caracteres). X
# - Domicilio (dirección).    X
# - Cuenta bancaria (puede ser una o varias) (11 dígitos). ESTO NO SE PONDRA AQUI: se pondrá en un nuevo modelo, y se
# meterá al Proveedor como una FK.)    X
# - CLABE (18 dígitos). ESTO NO SE PONDRA AQUI: se pondrá en un nuevo modelo, y se meterá al Proveedor como una FK.   X
# - Descuento (en porcentaje) (3 digitos enteros, 2 decimales maximo).   X
# - Calle, número exterior, número interior, colonia, código postal, ciudad, estado. (Le llamé "Dirección Fiscal"). X
# - Correo (uno o varios). NO SE DEBE AGREGAR AQUI. SE DEBE CREAR NUEVO MODELO.   X
# - Nombre del contacto. (100 caracteres) X
# - Telefono del contacto. (Varchar, 15 caracteres)  X
#
# * Datos fiscales de los proveedores:
# - RFC.  X
# - Razón social o nombre. (Lo puedo poner distinto al "Nombre del Contacto").    X
# - Calle, número ext., número int, colonia, código postal*, estado, ciudad.  X
# - Régimen fiscal* (es un catálogo te lo comparto).(FK)  X
# - Uso de CFDI* (es un catálogo). (FK)    X
# - Forma de pago* (es un catálogo).  (FK)    X
# - Método de pago* (catálogo).   (FK)    X
#
#
# Dado a que un descuento puede tener decimales (por ejemplo, con 10,5% de descuento), puedo poner máximo 5 dígitos: 3
# enteros con 2 decimales. Sería un DecimalField.
#
# Meteré todos los campos de la dirección fiscal dentro de un solo campo en el modelo de Proveedores.
#
# Dado que los teléfonos llevarán el prefijo “+”, les pondré un Varchar en lugar de integer. Pero aún así les pondré 15
# caracteres máximo.
#
# Respecto a Uso de CFDI con que pongas G01, G03 y S01 es suficiente.
#
# NO DEBO REPETIR LA RAZON SOCIAL 2 veces.
# """
#
#
# class Supplier(models.Model):
#
#     nombre_del_proveedor = models.CharField(blank=True, null=True, max_length=50)  # Nombre (Alias)
#     razon_social = models.CharField(max_length=100)     # Razon social
#
#     domicilio = models.TextField(max_length=350)  # Domicilio
#     descuento = models.DecimalField(max_digits=14, decimal_places=2)    # Descuento
#
#     # Datos Fiscales
#     rfc = models.CharField(max_length=13)  # Número RFC
#     direccion_fiscal = models.TextField(max_length=500)  # Dirección Fiscal
#
#     # # Razon Social o Nombre para Datos Fiscales
#     # razon_social_o_nombre_para_datos_fiscales = models.CharField(max_length=100)
#
#     # uso_cfdi = models.CharField(max_length=3)   # Uso de CFDI
#
#     # # Uso CFDI (FK)
#     # uso_cfdi = models.ForeignKey("UsoDeCFDI", on_delete=models.CASCADE,
#     #                              related_name="codigo_uso_cfdi_para_este_proveedor")
#
#     # # Forma De Pago (FK)
#     # forma_de_pago = models.ForeignKey("FormaDePago", on_delete=models.CASCADE,
#     #                              related_name="forma_de_pago_para_este_proveedor")
#     #
#     # # Método De Pago (FK)
#     # metodo_de_pago = models.ForeignKey("MetodoDePago", on_delete=models.CASCADE,
#     #                              related_name="metodo_de_pago_para_este_proveedor")
#     #
#     # # Régimen Fiscal (FK)
#     # regimen_fiscal = models.ForeignKey("RegimenFiscal", on_delete=models.CASCADE,
#     #                              related_name="regimen_fiscal_para_este_proveedor")
#     # Fin de los Datos Fiscales
#
#     nombre_del_contacto = models.CharField(max_length=100)  # Nombre del Contacto
#
#     # Teléfono del contacto
#     telefono_del_contacto = models.CharField(max_length=15)
#
#     # telefono_del_contacto = models.IntegerField(validators=[MaxValueValidator(999999999999999)])
#
#     # cuenta_bancaria = models.IntegerField(max_length=11)  # Número de Cuenta Bancaria. NO PUEDO USAR ESTO
#     #
#     # clabe = models.IntegerField(max_length=18)   # CLABE. NO PUEDO USAR ESTO
#
#     # Nombre en plural arreglado en el Panel de Admin de Django
#     class Meta:
#         verbose_name_plural = "Proveedores"
#
#     # Esto muestra el nombre del Proveedor junto con su RFC:
#     def __str__(self):
#         return f"{self.rfc} - {self.nombre_del_proveedor}"





# Wagtail Pages


# These will let me create a new page type in Wagtail (Source:
# https://docs.wagtail.org/en/stable/getting_started/tutorial.html). I will need to create a new class that inherits
# from Page, and then add fields to it. I will also need to create a template for the new page type, and then add a URL
# pattern to my URLS file.
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

# This will let me add a search index to my page type. I will need to add a search_fields attribute to my page type
# class, and then run a migration to create the search index.
from wagtail.search import index

# I need all this libraries to create all the functionalities for the Product Registration Page
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# from wagtail.core.models import Page
# from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
# from wagtail.contrib.forms.views import process_form_submission

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# New imports added for ParentalKey, Orderable, InlinePanel
# Add these:
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

# This will let me import all the blog pages in the blog_page.html for the side navbar.
from django.shortcuts import render

# This will let me use the Paginator class to paginate the blog entries in the Blog Index Page.
from django.core.paginator import Paginator

from wagtail.images.models import Image




# # This takes all my forms from my forms.py file. I NEED TO CHANGE THE NAMES OF THE FORMS LATER.
# from .forms import FormularioRegistrarProductos, FormsetImagenesSecundariasParaUnProducto

# # These are the models that I'll need to use. I NEED TO CREATE THESE MODELS LATER.
# from .models import Producto, PrecioDeCompraDelProveedor, ImagenSecundariaDeUnProducto



from django.core.exceptions import ObjectDoesNotExist
import datetime


# This is the Index page for the Dashboard for Employees app . This will be the parent page for all of my blog posts.
class DashboardIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


""" Test page to insert as a Child Element of the Dashboard Index Page. DELETE LATER.
"""
class DashboardPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]


""" Artwork Index Page. This is the "view" that renders the page that displays the List of all my Images 
generated using Stable Diffusion.

Here's a general algorithm to add pagination to your Wagtail page:

Import the Paginator class from Django's core paginator module at the top of your models.py file.

In the get_context method of your ArtworkIndexPage class, after retrieving the artworkpages queryset, create a Paginator 
object. The Paginator object takes two arguments: the list or queryset to paginate, and the number of items per page.

Get the page number from the request's GET parameters. If the page parameter is not present, default to the first page.

Use the Paginator's get_page method to retrieve the Page object for the current page. This method will automatically 
handle invalid page numbers and out of range errors by returning the first or last page respectively.

Add the Page object to the context dictionary under the 'artworkpages' key.

In your template, you can now loop over the 'artworkpages' context variable to display the artworks / images for the current 
page. You can also use the Page object's has_previous, has_next, previous_page_number, and next_page_number methods to 
display navigation links.
"""


class ArtworkIndexPage(Page):
    intro = RichTextField(blank=True)

    # # Add the get_context method
    # def get_context(self, request):
    #     # Update context to include only published posts, ordered by reverse-chron
    #     context = super().get_context(request)
    #     productpages = self.get_children().live().order_by('-first_published_at')
    #
    #     # Create a Paginator object to add Pagination. This way, if there are more than 10 products, the page will
    #     # display only 10 products at a time, and the user can navigate to the next page to see the rest of the entries.
    #     paginator = Paginator(productpages, 10)  # Show 10 blog entries per page
    #
    #     # Get the page number from the request
    #     page = request.GET.get('page')
    #
    #     # Get the Page object for the current page
    #     productpages = paginator.get_page(page)
    #
    #     # Add the Page object to the context. "productpages" is like the Jinja variable that contains all of the blog
    #     # entries from the Query Set.
    #     context['productpages'] = productpages
    #
    #     # This is like the "return render request" from he traditional Django views.
    #     return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]


""" Artwork Page. This is the "view" that renders the detailed page that displays the Image. 

Here's where you'll be able to see the prompts used for creating the image, the date it was created, the image itself, 
the AI use for creating it, etc.

To add image upload functionality to the ArtworkPage model, you can create a new model similar to BlogPageGalleryImage. 
This new model, which we can call ArtworkPageGalleryImage, will represent an image in a gallery of images for an artwork 
page.

Below the ArtworkPage model, I will create a new model called ArtworkPageGalleryImage. This new model will have a 
Foreign Key to Wagtail's own Image model, a caption field, and will take the ArtworkPage model (this page) as an FK
(or Parental Key, as it's called in Wagtail).

COPYRIGHT_CHOICES is a list of tuples that define the choices available in the dropdown menu. The copyright field is a 
CharField with choices=COPYRIGHT_CHOICES, which creates a dropdown menu with the options defined in COPYRIGHT_CHOICES. 
The default='No' argument sets the default value of the dropdown menu to 'No'. The FieldPanel('copyright') line adds a 
panel to the Wagtail admin interface for the copyright field, allowing it to be edited.
"""


class ArtworkPage(Page):

    # This is for the dropdown menu that will ask the user if the image has copyright content
    COPYRIGHT_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    # These are the choices for the dropdown menu to select the AI used for creating the image
    AI_CHOICES = [
        ('Midjourney', 'Midjourney'),
        ('Bing / Copilot Designer', 'Bing / Copilot Designer'),
        ('DALL-E', 'DALL-E'),
        ('Ideogram', 'Ideogram'),
        ('Other', 'Other'),
    ]

    # Date of the image. The text "Image date" is like the verbose name / label from traditional Django models.
    date = models.DateField("Image date")
    intro = models.CharField(max_length=250)

    # This will store the prompts
    prompt = RichTextField(blank=True)

    # Does the image have any form of copyright content?
    copyright = models.CharField(max_length=3, choices=COPYRIGHT_CHOICES, default='No',
                                 verbose_name="Does it have copyright content?")

    # Please, explain why this image has copyright content. OPTIONAL
    explanation = models.TextField(blank=True, null=True, verbose_name="Please, elaborate")

    # AI used to create the image. It needs to be a Dropdown Menu.
    ai_used = models.CharField(max_length=100, choices=AI_CHOICES, default='Midjourney', verbose_name="AI used")

    # Specify the name of the AI if the AI selected is "Other" (OPTIONAL)
    specify_ai_if_other = models.CharField(max_length=100, blank=True, null=True, verbose_name="Specify AI if 'Other'")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('prompt'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('prompt'),
        FieldPanel('copyright'),    # Dropdown Menu that asks if the image has copyright content.
        FieldPanel('explanation'),  # Optional field to explain why the image has copyright content.
        FieldPanel('ai_used'),      # Dropdown Menu that asks which AI was used to create the image.
        FieldPanel('specify_ai_if_other'),  # Field to specify the name of the AI if the AI selected is "Other".
        # This will allow me to upload images. I think this comes from ArtworkPageGalleryImage().
        InlinePanel('gallery_images', label="Gallery images"),
    ]


""" Artwork Page Gallery Image model.

This is a new model that represents an image in a gallery of images for an artwork page. It has a 
ParentalKey to the ArtworkPage model, which means each ArtworkPage can have multiple ArtworkPageGalleryImage instances 
associated with it. The image field is a ForeignKey to the Image model provided by Wagtail, which means each 
ArtworkPageGalleryImage instance can be associated with an image uploaded via the Wagtail admin interface. The caption 
field can store a caption for the image.  The InlinePanel('gallery_images', label="Gallery images") line in the 
ArtworkPage model's content_panels list allows you to add, edit, and remove gallery images from the Wagtail admin 
interface when editing an ArtworkPage. 

The "wagtailimages.Image" model is a pre-installed Wagtail model that allows me to store images in the Wagtail admin 
interface.

The Orderable class, which is a special Django model provided by Wagtail that allows the instances of the model to be 
ordered in a specific sequence. 
"""


class ArtworkPageGalleryImage(Orderable):

    # A Parental Key is pretty similar to the Wagtail version of an FK. This is taking the Artwork Page as an FK.
    page = ParentalKey(ArtworkPage, on_delete=models.CASCADE, related_name='gallery_images')

    # This is the actual image. This is a ForeignKey to the Image model provided by Wagtail.
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    # This is the panel that will appear in the Wagtail admin interface when editing an Artwork Page.
    panels = [

        # This will let me select an image to upload.
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

















""" Product Index Page. This is the "view" that renders the page that displays the List of Products.

Here's a general algorithm to add pagination to your Wagtail page:

Import the Paginator class from Django's core paginator module at the top of your models.py file.

In the get_context method of your BlogIndexPage class, after retrieving the blogpages queryset, create a Paginator 
object. The Paginator object takes two arguments: the list or queryset to paginate, and the number of items per page.

Get the page number from the request's GET parameters. If the page parameter is not present, default to the first page.

Use the Paginator's get_page method to retrieve the Page object for the current page. This method will automatically 
handle invalid page numbers and out of range errors by returning the first or last page respectively.

Add the Page object to the context dictionary under the 'blogpages' key.

In your template, you can now loop over the 'productpages' context variable to display the blog entries for the current 
page. You can also use the Page object's has_previous, has_next, previous_page_number, and next_page_number methods to 
display navigation links.
"""


class ProductIndexPage(Page):
    intro = RichTextField(blank=True)

    # # Add the get_context method
    # def get_context(self, request):
    #     # Update context to include only published posts, ordered by reverse-chron
    #     context = super().get_context(request)
    #     productpages = self.get_children().live().order_by('-first_published_at')
    #
    #     # Create a Paginator object to add Pagination. This way, if there are more than 10 products, the page will
    #     # display only 10 products at a time, and the user can navigate to the next page to see the rest of the entries.
    #     paginator = Paginator(productpages, 10)  # Show 10 blog entries per page
    #
    #     # Get the page number from the request
    #     page = request.GET.get('page')
    #
    #     # Get the Page object for the current page
    #     productpages = paginator.get_page(page)
    #
    #     # Add the Page object to the context. "productpages" is like the Jinja variable that contains all of the blog
    #     # entries from the Query Set.
    #     context['productpages'] = productpages
    #
    #     # This is like the "return render request" from he traditional Django views.
    #     return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]


""" Product Registration Form Page. This is the "view" with the Form to create new products. 

This new `Page` model will represent the product registration page.

In Wagtail, the logic that would normally be in a Django view is often moved into the `Page` model itself. For example, 
the form handling logic can be moved into the `serve` method of the `Page` model.
"""
