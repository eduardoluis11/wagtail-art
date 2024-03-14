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

"""
class Product(models.Model):
    product_name = models.CharField(max_length=200)  # Product Name

    sku_code = models.CharField(max_length=40, unique=True)  # SKU (Stock Keeping Unit) Code
    description = models.CharField(max_length=500)  # Description
    unit_of_measurement = models.CharField(max_length=20)  # Unit of Measurement
    category = models.CharField(max_length=100)    # Category
    list_price = models.DecimalField(max_digits=14, decimal_places=2)  # List Price

    # # Purchase Price (defined by supplier but modifiable). CREATE MODEL LATER.
    # purchase_price = models.ForeignKey('SupplierPurchasePrice', on_delete=models.CASCADE)

    # Sale Price (same as list price, initially)
    sale_price = models.DecimalField(max_digits=14, decimal_places=2)  # Sale Price

    main_image = models.ImageField(upload_to='products/main-images')    # Main Image

    # Technical Sheet (Optional)
    technical_sheet = models.FileField(upload_to='products/technical-sheets', blank=True, null=True)

    # This displays the Product's name and SKU code
    def __str__(self):
        return f"{self.product_name} - SKU: {self.sku_code}"





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
