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
    date = models.DateField("Image date")

    # This adds a short description for the Artwork
    intro = models.CharField(max_length=250)

    # This will store the prompts used for creating the Artwork
    prompt = models.TextField(blank=True)

    # Does the image have any form of copyright content?
    copyright = models.CharField(max_length=3, choices=COPYRIGHT_CHOICES, default='No',
                                 verbose_name="Does it have copyright content?")

    # Please, explain why this image has copyright content. OPTIONAL
    explanation = models.TextField(blank=True, null=True, verbose_name="Please, elaborate")

    # AI used to create the image. It needs to be a Dropdown Menu.
    ai_used = models.CharField(max_length=100, choices=AI_CHOICES, default='Midjourney', verbose_name="AI used")

    # Specify the name of the AI if the AI selected is "Other" (OPTIONAL)
    specify_ai_if_other = models.CharField(max_length=100, blank=True, null=True, verbose_name="Specify AI if 'Other'")
