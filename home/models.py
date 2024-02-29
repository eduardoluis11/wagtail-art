# Source of this code: Official Wagtail tutorial from https://docs.wagtail.org/en/stable/getting_started/tutorial.html 

from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel




class HomePage(Page):
    # add the Hero section of the HomePage:
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image"
    )
    hero_text = models.CharField(
        blank=True,
        max_length=255,
        help_text="Write an introduction for the site"
    )
    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to action"
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA Link",
        help_text="Choose a page to link to for the Call to Action",
    )

    body = RichTextField(blank=True)

    # Modify your content_panels:
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('image'),
            FieldPanel('hero_text'),
            FieldPanel('hero_cta'),
            FieldPanel('hero_cta_link'),
        ], heading="Hero section",
        ),
        FieldPanel('body'),
    ]

    # content_panels = Page.content_panels + [
    #     FieldPanel('body'),
    # ]
