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

    # This will store the prompts used for creating the Artwork
    prompt = forms.CharField()
    #
    # # Does the image have any form of copyright content?
    # copyright = forms.CharField(max_length=3, choices=COPYRIGHT_CHOICES, default='No',
    #                              verbose_name="Does it have copyright content?")

    # Please, explain why this image has copyright content. OPTIONAL
    explanation = forms.CharField(required=False, label="Please, elaborate")

    # # AI used to create the image. It needs to be a Dropdown Menu.
    # ai_used = forms.CharField(max_length=100, choices=AI_CHOICES, default='Midjourney', label="AI used")

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

