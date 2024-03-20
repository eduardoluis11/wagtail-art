""" Here are all the Forms that I'll use in my web app.

"""
# This will let me use Django forms
from django import forms

# This will let me use dats
from datetime import date

# This will let me use Formsets
from django.forms import formset_factory

# This will let me use Django's models
from django.db import models

# This will import the specific models that I'll need to use in my forms
# from .models import ArtworkPage

""" Form for Adding a New Product.

All the basic data for each product will be stored in this model.

Then, in the model called "Products of an Order," I will call the FK with the product selected by the user and add as
additional fields the selected quantity (for example, "3" if they want to buy 3 containers) and the order to which
that quantity of products belongs (as a FK). I could also include the subtotal. But for now, the only thing I need
in the Product Model of a Purchase Order is the quantity of products ordered in a purchase order.

#### Fields:
- Main Image* PNG. (ImageField).
** Secondary Images: I will create a new model to assign multiple secondary images to each product, as a product can
have several secondary images. This will be a Formset. However, they would still be uploaded in Wagtail's Image
model, the same model where the Main Image would be uploaded.

* Technical Sheet (File). (FileField).
* Product Name*
* Unit Price. (THIS DOES NOT GO HERE, and it is REDUNDANT. I already have about 3 prices here).
* SKU (Stock Keeping Unit)* (40 characters).
* Description* (text) (500 characters).
* Unit of Measurement* (Piece, service, box) -> I'll send you the catalog.
* Category* -> CRUD. Apparently, the user can write whatever they want here. I'll put it as Varchar, 100 characters.
* List Price* (100 EUR) (I think "EUR" stands for "euros") (14 digits with 2 decimals).
* Purchase Price* (percentage defined by supplier but modifiable) (one to many) (FK).
* Sale Price* (same as list) 100 EUR. There is no difference between this and the "List Price." They must be exactly
the same price. In the future, this field will be modified to make them different.


Only the very first two fields will actually be done in here. The rest of the fields will be directly created on 
Wagtail's Admin Panel. That is because, out of all the fields, Wagtail's forms aren't very good at handling file 
uploads.

As for the Technical Sheets: do T-shirt suppliers even give you technical sheets? I'm going to sell T-shirts, so I don't
think I'll need that field.

There is only one supplier that offers a volume discount. The rest have a price per product. Normally it's 28% - 10% 
(35.2%).

I think of creating a model called "Supplier Purchase Prices," and I will take the records from that model as FK in the
"Purchase Price" field in the Product model. That model I will create will have only and exclusively the purchase prices from
the suppliers. I don't think it will be a percentage, but rather a normal price, only that the discount from that specific
supplier is already applied to it.

The SKU field must be unique for each product. There cannot be 2 products with the same SKU. Therefore, I put a restriction
on it with the "unique" keyword.

To prevent any confusions, I will call "Product From the Supplier" to the "Suplier Purchase Prices" model. In reality,
that's what that model is: it stores the products offered by that supplier.

Remember that these are form fields, NOT MODELS. I won't specify the folder on my "media" folder where I'll upload
these images nor files in here. I'll do that in the models.py file.

"""


class AddProductForm(forms.Form):
    # product_name = forms.CharField(max_length=200)  # Product Name
    #
    # sku_code = forms.CharField(max_length=40)  # SKU (Stock Keeping Unit) Code
    # description = forms.CharField(max_length=500)  # Description
    # unit_of_measurement = forms.CharField(max_length=20)  # Unit of Measurement
    # category = forms.CharField(max_length=100)    # Category
    # list_price = forms.DecimalField(max_digits=14, decimal_places=2)  # List Price

    # # Purchase Price (defined by supplier but modifiable)
    # purchase_price = forms.ForeignKey('ProductFromTheSupplier', on_delete=models.CASCADE)

    # # Sale Price (same as list price, initially)
    # sale_price = forms.DecimalField(max_digits=14, decimal_places=2)  # Sale Price

    # main_image = forms.ImageField(upload_to='products/main-images')    # Main Image
    main_image = forms.ImageField()    # Main Image

    # # Technical Sheet (Optional)
    # technical_sheet = forms.FileField(required=False)
    # technical_sheet = forms.FileField(upload_to='products/technical-sheets', required=False)

    # I will later create a field for the Secondary Images.


""" Form for adding a new Artwork made with stable diffusion to the Artwork Page model.

It needs to have the exact same fields as the Artwork Page model.

Fields:
- Date of the image (DateField). 
- Short Description of the Image (Intro) (CharField, 250 characters).
- Prompts used for creating the image (TextField).
- Does the image have any form of copyright content? (MultipleChoice, 3 characters, default, "No").
- Please, explain why this image has copyright content. OPTIONAL (TextField).
- AI used to create the image (MultipleChoice, 100 characters, default, "Midjourney").
- Specify the name of the AI if the AI selected is "Other" (OPTIONAL) (CharField, 100 characters).

Ideally, I should also have a formset for adding multiple images. However, to not to make things too complicated, I'll 
just add one image for now.

Remember that Django forms use "forms.Type_of_Field" to create the fields, NOT "models.Type_of_Field"!
"""


class AddArtworkForm(forms.Form):
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
    date = forms.DateField(label="Image date")

    # This adds a short description for the Artwork
    intro = forms.CharField(max_length=250)

    # This is the image itself. I WON'T USE A FORMSET YET.
    image = forms.ImageField()

    # This will store the prompts used for creating the Artwork
    prompt = forms.CharField()

    # Does the image have any form of copyright content?
    copyright = forms.ChoiceField(choices=COPYRIGHT_CHOICES, initial='No',
                                  label="Does it have copyright content?")

    # Please, explain why this image has copyright content. OPTIONAL
    explanation = forms.CharField(required=False, label="Please, elaborate")

    # AI used to create the image. It needs to be a Dropdown Menu.
    ai_used = forms.ChoiceField(choices=AI_CHOICES, initial='Midjourney', label="AI used")

    # Specify the name of the AI if the AI selected is "Other" (OPTIONAL)
    specify_ai_if_other = forms.CharField(max_length=100, required=False, label="Specify AI if 'Other'")








# class FormularioRegistrarProductos(forms.Form):
#     # Nombre del Producto
#     nombre_del_producto = forms.CharField(max_length=200,
#                                           widget=forms.TextInput(attrs={'class': 'form-control-customizado'}),
#                                           label="Nombre del Producto *")
#
#     # # <label> del Nombre del Producto
#     # nombre_del_producto.label_class = 'form-label'
#
#     # Clave (SKU)
#     clave_sku = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control-customizado'}),
#                                 label="Clave (SKU) *")
#
#     # Descripción
#     descripcion = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control-customizado'}),
#                                   label="Descripción *")
#
#     # Unidad de medida
#     unidad_de_medida = forms.CharField(max_length=20,
#                                        widget=forms.TextInput(attrs={'class': 'form-control-customizado'}),
#                                        label="Unidad de Medida *")
#
#     # Categoría
#     categoria = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-customizado'}),
#                                 label="Categoría *")
#
#     # Precio de Lista
#     precio_de_lista = forms.DecimalField(max_digits=14, decimal_places=2,
#                                          widget=forms.NumberInput(attrs={'class': 'form-control-customizado'}),
#                                          label="Precio de Lista *")
#
#     # Precio de Compra (OPCIONAL)
#     precio_de_compra = forms.DecimalField(required=False, max_digits=14, decimal_places=2,
#                                           widget=forms.NumberInput(attrs={'class': 'form-control-customizado'}))
#
#     # precio_de_compra = forms.ModelChoiceField(queryset=PrecioDeCompraDelProveedor.objects.all(),
#     #                                           widget=forms.Select(attrs={'class': 'ancho-de-menus-desplegables'}))
#
#     # # Esto me creará un menú desplegable con el Proveedor como Foreign Key del modelo de Proveedores (OPCIONAL)
#     # proveedor = forms.ModelChoiceField(required=False, queryset=Proveedor.objects.all())
#
#     # # Precio de compra (FK)
#     # precio_de_compra = models.ForeignKey("PrecioDeCompraDelProveedor", on_delete=models.CASCADE,
#     #                              related_name="precio_de_compra_del_proveedor")
#
#     # Precio de Venta
#     precio_de_venta = forms.DecimalField(max_digits=14, decimal_places=2,
#                                          widget=forms.NumberInput(attrs={'class': 'form-control-customizado'}),
#                                          label="Precio de Venta *")
#     # Imagen Principal
#     imagen_principal = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-customizado'}),
#                                         label="Imagen Principal *")
#
#     # # Imagen Secundaria (Opcional) (FORMSET)
#     # imagen_secundaria = forms.ImageField(required=False)
#
#     # Ficha Técnica (Opcional)
#     ficha_tecnica = forms.FileField(required=False,
#                                     widget=forms.ClearableFileInput(attrs={'class': 'form-control-customizado'}))

