from django.db import models

# Create your models here.

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


# This is the Index page for the Dashboard for Employees app . This will be the parent page for all of my blog posts.
class DashboardIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
