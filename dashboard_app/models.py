from django.db import models

# Create your models here.

""" ### Product Model

All the basic data for each product will be stored in this model.

Then, in the model called "Products of an Order," I will call the FK with the product selected by the user and add as 
additional fields the selected quantity (for example, "3" if they want to buy 3 containers) and the order to which 
that quantity of products belongs (as a FK). I could also include the subtotal. But for now, the only thing I need 
in the Product Model of a Purchase Order is the quantity of products ordered in a purchase order.

#### Fields:
- Product Name*
- Unit Price. (THIS DOES NOT GO HERE, and it is REDUNDANT. I already have about 3 prices here).
- SKU (Stock Keeping Unit)* (40 characters).
- Description* (text) (500 characters).
- Unit of Measurement* (Piece, service, box) -> I'll send you the catalog.
- Category* -> CRUD. Apparently, the user can write whatever they want here. I'll put it as Varchar, 100 characters.
- List Price* (100 EUR) (I think "EUR" stands for "euros") (14 digits with 2 decimals).
- Purchase Price* (percentage defined by supplier but modifiable) (one to many) (FK).
- Sale Price* (same as list) 100 EUR. There is no difference between this and the "List Price." They must be exactly 
the same price. In the future, this field will be modified to make them different.
- Main Image* PNG. (ImageField).
- Technical Sheet (File). (FileField).

* Secondary Images: I will create a new model to assign multiple secondary images to each product, as a product can 
have several secondary images.

There is only one supplier that offers a volume discount. The rest have a price per product. Normally it's 28% - 10% (35.2%).

I think of creating a model called "Supplier Purchase Prices," and I will take the records from that model as FK in the 
"Purchase Price" field in the Product model. That model I will create will have only and exclusively the purchase prices from 
the suppliers. I don't think it will be a percentage, but rather a normal price, only that the discount from that specific 
supplier is already applied to it.

The SKU field must be unique for each product. There cannot be 2 products with the same SKU. Therefore, I put a restriction 
on it with the "unique" keyword.

To prevent any confusions, I will call "Product From the Supplier" to the "Supllier Purchase Prices" model. In reality, 
that's what that model is: it stores the products offered by that supplier.
"""


class Product(models.Model):
    product_name = models.CharField(max_length=200)  # Product Name

    sku_code = models.CharField(max_length=40, unique=True)  # SKU (Stock Keeping Unit) Code
    description = models.CharField(max_length=500)  # Description
    unit_of_measurement = models.CharField(max_length=20)  # Unit of Measurement
    category = models.CharField(max_length=100)    # Category
    list_price = models.DecimalField(max_digits=14, decimal_places=2)  # List Price

    # Purchase Price (defined by supplier but modifiable)
    purchase_price = models.ForeignKey('ProductFromTheSupplier', on_delete=models.CASCADE)

    # Sale Price (same as list price, initially)
    sale_price = models.DecimalField(max_digits=14, decimal_places=2)  # Sale Price

    main_image = models.ImageField(upload_to='products/main-images')    # Main Image

    # Technical Sheet (Optional)
    technical_sheet = models.FileField(upload_to='products/technical-sheets', blank=True, null=True)

    # This displays the Product's name and SKU code
    def __str__(self):
        return f"{self.product_name} - SKU: {self.sku_code}"



""" Modelo con los Precios de Compra de los Proveedores.

Dado a que un producto del modelo de Productos puede tener uno o varios precios de compra, tengo que crear este modelo.
Así aquí puedo almacenar todos los precios de compra como registros en este modelo, y se le pueden asignar varios
precios de compra a un solo producto usando una FK de este model en el modelo de Productos.

Dado a que cada proveedor define su propio precio de compra, creo que pondré otro campo llamado "proveedor". Ese campo
debería ser una FK del modelo de Proveedores.

*Campos:
- Precio de Compra (14 dígitos con 2 decimales).
- Proveedor (FK).
- Producto (FK)

El "locale" y el "format_string" va a imprimirme el precio en pesos mexicanos, en donde se mostraran los decimales con 
comas en el panel de admin de Django y cuando se imprima el precio de compra como Foreign Key. Así se debe hacer en
español.

Por motivos de user experience, le cambiare el Meta del modelo “Precios de Compra de los Proveedores” a “Productos de 
los Proveedores”. Eso es para evitar confusiones.

Solo haré que el producto sea obligatorio. TANTO EL PRECIO DE COMPRA COMO EL PROVEEDOR DEBEN SER OPCIONALES.
"""


class ProductFromTheSupplier(models.Model):

    # Proveedor que ofrece este precio
    proveedor = models.ForeignKey("Supplier", on_delete=models.CASCADE, related_name="proveedor_de_este_precio",
                                  null=True, blank=True)

    # Producto (FK)
    producto = models.ForeignKey("Product", on_delete=models.CASCADE,
                                 related_name="producto_que_tiene_este_precio_de_compra")

    # Precio de Compra
    precio_de_compra = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Precio de compra ($)",
                                           null=True, blank=True, default=0)

    # Nombre en plural arreglado en el Panel de Admin de Django
    class Meta:
        verbose_name_plural = "Productos de los Proveedores"

    # Esto muestra el precio de compra, junto con el nombre del proveedor.
    def __str__(self):
        return (f"{self.producto.product_name} - {self.proveedor} - "
                f"${self.precio_de_compra}")


""" Modelo de Proveedores.

* Campos:
- Nombre del Proveedor (Alias) (ej: Umbrella).  X
- Razón social (ej: Umbrella Corp). X
- RFC (y Datos Fiscales (PREGUNTAR QUE ES ESTO DE DATOS FISCALES)) (ej: XAXX010101000) (13 caracteres). X
- Domicilio (dirección).    X
- Cuenta bancaria (puede ser una o varias) (11 dígitos). ESTO NO SE PONDRA AQUI: se pondrá en un nuevo modelo, y se 
meterá al Proveedor como una FK.)    X
- CLABE (18 dígitos). ESTO NO SE PONDRA AQUI: se pondrá en un nuevo modelo, y se meterá al Proveedor como una FK.   X  
- Descuento (en porcentaje) (3 digitos enteros, 2 decimales maximo).   X
- Calle, número exterior, número interior, colonia, código postal, ciudad, estado. (Le llamé "Dirección Fiscal"). X
- Correo (uno o varios). NO SE DEBE AGREGAR AQUI. SE DEBE CREAR NUEVO MODELO.   X
- Nombre del contacto. (100 caracteres) X
- Telefono del contacto. (Varchar, 15 caracteres)  X

* Datos fiscales de los proveedores:
- RFC.  X
- Razón social o nombre. (Lo puedo poner distinto al "Nombre del Contacto").    X
- Calle, número ext., número int, colonia, código postal*, estado, ciudad.  X
- Régimen fiscal* (es un catálogo te lo comparto).(FK)  X
- Uso de CFDI* (es un catálogo). (FK)    X
- Forma de pago* (es un catálogo).  (FK)    X
- Método de pago* (catálogo).   (FK)    X


Dado a que un descuento puede tener decimales (por ejemplo, con 10,5% de descuento), puedo poner máximo 5 dígitos: 3 
enteros con 2 decimales. Sería un DecimalField.

Meteré todos los campos de la dirección fiscal dentro de un solo campo en el modelo de Proveedores.

Dado que los teléfonos llevarán el prefijo “+”, les pondré un Varchar en lugar de integer. Pero aún así les pondré 15 
caracteres máximo.

Respecto a Uso de CFDI con que pongas G01, G03 y S01 es suficiente.

NO DEBO REPETIR LA RAZON SOCIAL 2 veces.
"""


class Supplier(models.Model):

    nombre_del_proveedor = models.CharField(blank=True, null=True, max_length=50)  # Nombre (Alias)
    razon_social = models.CharField(max_length=100)     # Razon social

    domicilio = models.TextField(max_length=350)  # Domicilio
    descuento = models.DecimalField(max_digits=14, decimal_places=2)    # Descuento

    # Datos Fiscales
    rfc = models.CharField(max_length=13)  # Número RFC
    direccion_fiscal = models.TextField(max_length=500)  # Dirección Fiscal

    # # Razon Social o Nombre para Datos Fiscales
    # razon_social_o_nombre_para_datos_fiscales = models.CharField(max_length=100)

    # uso_cfdi = models.CharField(max_length=3)   # Uso de CFDI

    # # Uso CFDI (FK)
    # uso_cfdi = models.ForeignKey("UsoDeCFDI", on_delete=models.CASCADE,
    #                              related_name="codigo_uso_cfdi_para_este_proveedor")

    # # Forma De Pago (FK)
    # forma_de_pago = models.ForeignKey("FormaDePago", on_delete=models.CASCADE,
    #                              related_name="forma_de_pago_para_este_proveedor")
    #
    # # Método De Pago (FK)
    # metodo_de_pago = models.ForeignKey("MetodoDePago", on_delete=models.CASCADE,
    #                              related_name="metodo_de_pago_para_este_proveedor")
    #
    # # Régimen Fiscal (FK)
    # regimen_fiscal = models.ForeignKey("RegimenFiscal", on_delete=models.CASCADE,
    #                              related_name="regimen_fiscal_para_este_proveedor")
    # Fin de los Datos Fiscales

    nombre_del_contacto = models.CharField(max_length=100)  # Nombre del Contacto

    # Teléfono del contacto
    telefono_del_contacto = models.CharField(max_length=15)

    # telefono_del_contacto = models.IntegerField(validators=[MaxValueValidator(999999999999999)])

    # cuenta_bancaria = models.IntegerField(max_length=11)  # Número de Cuenta Bancaria. NO PUEDO USAR ESTO
    #
    # clabe = models.IntegerField(max_length=18)   # CLABE. NO PUEDO USAR ESTO

    # Nombre en plural arreglado en el Panel de Admin de Django
    class Meta:
        verbose_name_plural = "Proveedores"

    # Esto muestra el nombre del Proveedor junto con su RFC:
    def __str__(self):
        return f"{self.rfc} - {self.nombre_del_proveedor}"





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

""" Product Registration Page.

This new `Page` model will represent the product registration page.

In Wagtail, the logic that would normally be in a Django view is often moved into the `Page` model itself. For example, 
the form handling logic can be moved into the `serve` method of the `Page` model.
"""
