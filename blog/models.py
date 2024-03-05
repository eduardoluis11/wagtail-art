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
