# Source of the code: https://docs.wagtail.org/en/stable/getting_started/tutorial.html

# New imports added for forms and ParentalManyToManyField, and MultiFieldPanel
from django import forms
from django.db import models

# New imports added for ClusterTaggableManager, TaggedItemBase

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

# ... Keep BlogIndexPage, BlogPage, BlogPageGalleryImage models, and then add the Author model:


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"


# Create your models here.
# keep the definition of BlogIndexPage model, and add the BlogPage model:
# Keep the definition of BlogIndexPage, update the content_panels of BlogPage, and add a new BlogPageGalleryImage model:

# ... Keep the definition of BlogIndexPage model and add a new BlogPageTag model

""" Tags for the "view" that renders each specific Blog Entry. 
"""


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


""" Tags for the Blog Index Page.

You need to create a new through model for BlogIndexPage. Let's call it BlogIndexPageTag. This model will have a 
content_object field that is a ParentalKey to BlogIndexPage. Then, in BlogIndexPage, you should use 
ClusterTaggableManager(through=BlogIndexPageTag, blank=True) instead of ClusterTaggableManager(through=BlogPageTag, 
blank=True).
"""


class BlogIndexPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogIndexPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


""" This is the "view" that rendered the page that displays all the blog entries. That is, this is the Blog Index Page.

I want to add tags to this page.

To get the Tags, I need to use "BlogIndexPageTag" instead of "BlogPageTag" in the BlogIndexPage model. The 
BlogIndexPageTag is the through model for the tags of the Blog Index Page. Meanwhile, the BlogPageTag is the through
model for the tags of the Blog Entry pages (the "view" for each individual Blog Entry page). That's why I get a bug if
I use the BlogPageTag instead of the BlogIndexPageTag for the "tags" field.

To add tags to the BlogIndexPage model, you can follow a similar approach as the BlogPage model. You need to add a
 ClusterTaggableManager field to the BlogIndexPage model and update the content_panels to include the tags field.
 
In this code, tags = ClusterTaggableManager(through=BlogPageTag, blank=True) adds a tags field to the BlogIndexPage 
model. The through=BlogPageTag argument specifies the model that will be used to store the tags. The blank=True 
argument allows the tags field to be empty.  The FieldPanel('tags') line in content_panels allows the tags to be edited 
in the Wagtail admin interface.
"""


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    # Add the "tags" field using the Tags for the Blog Index Page, NOT for the individual Blog Entry pages.
    tags = ClusterTaggableManager(through=BlogIndexPageTag, blank=True)

    # Add the get_context method
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('tags'),
    ]



""" This is the "view" that rendered the page each specific Blog Entry.

Modify the BlogPage model.

To pass the blogpages variable to the blog_page.html template, you need to modify the serve method in your BlogPage 
model. The serve method is called when a request is made to a page's URL. By overriding this method, you can add 
additional context variables to the template. 

In this code, BlogPage.objects.all() is used to retrieve all blog pages. You might want to replace this with a more 
specific query depending on your needs. The serve method then renders the blog_page.html template and passes the 
current page (self) and the blogpages variable to the template.
"""


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)

    # This adds the tags so that I can render the tags in the Wagtail admin panel:
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    # Add the main_image method:
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # ... Keep the main_image method and search_fields definition. Modify your content_panels:
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),

            # Add this:
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    # This will sent the blogpages variable with the most recent blog entries to the blog_page.html template:
    def serve(self, request):
        # Retrieve all blog pages, and sort them by date (from most recent to oldest)
        blogpages = BlogPage.objects.all().order_by('-first_published_at')

        # Render the template
        return render(request, 'blog/blog_page.html', {
            'page': self,
            'blogpages': blogpages,
        })  # End of the snippet that sends the blogpages variable to the blog_page.html template.


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


""" This is a page similar to the "Search" page, but that displays all the blog entries that have the tag
that you clicked on. This is just a list of results of blog entries with a selected tag. This is NOT the  Blog Index
Page.
"""


class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


""" Terms and Conditions "view", that is, this is the Terms and Conditions page.

To create a simple "Terms and Conditions" page in your Wagtail project, you can follow these steps:  

1) Create a new model for the "Terms and Conditions" page in your blog/models.py file. This model will inherit from the 
Page model provided by Wagtail. You can add a RichTextField to this model to store the content of the "Terms and 
Conditions" page.
  
2) Register the new model in the Wagtail admin interface by adding it to the content_panels attribute.  

3) Create a new template for the "Terms and Conditions" page in your blog/templates/blog directory.

After creating the model and the template, you can create a new "Terms and Conditions" page from the Wagtail admin 
interface. The content of the page can be edited using the rich text editor provided by Wagtail.
"""


class TermsAndConditionsPage(Page):
    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
    ]


""" Privacy Policy "view", that is, this is the Privacy Policy page.
"""


class PrivacyPolicyPage(Page):
    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
    ]
