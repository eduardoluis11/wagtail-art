""" I used code from this source: https://docs.wagtail.org/en/stable/tutorial/create-footer_for_all_pages.html

I also used some code from this source: https://docs.wagtail.org/en/stable/tutorial/create_contact_page.html

"""

from django.db import models

# import parentalKey:
from modelcluster.fields import ParentalKey

from modelcluster.models import ClusterableModel

# import FieldRowPanel and InlinePanel:
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)

# import RichTextField
from wagtail.fields import RichTextField

# import DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin:
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)

# import AbstractEmailForm and AbstractFormField:
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
)

# import FormSubmissionsPanel:
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.snippets.models import register_snippet


# ... keep the definition of NavigationSettings and FooterText. Add FormField and FormPage:
class FormField(AbstractFormField):
    page = ParentalKey(
        "FormPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Add a class to each field in the form
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("from_address"),
                FieldPanel("to_address"),
            ]),
            FieldPanel("subject"),
        ], "Email"),
    ]


# Create your models here.


""" This adds a new page in the Wagtail Admin Panel in the "Settings" section called "Navigation Settings", which
is where I'll be able to type the URL for my Social Media Accounts. I won't type my social media accounts directly
in my code. Instead, I will add it from the Wagtail Admin panel.

"""


@register_setting
class NavigationSettings(BaseGenericSetting):
    twitter_url = models.URLField(verbose_name="Twitter URL", blank=True)
    github_url = models.URLField(verbose_name="Github URL", blank=True)
    facebook_url = models.URLField(verbose_name="Facebook URL", blank=True)
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('twitter_url'),
                FieldPanel('github_url'),
                FieldPanel('facebook_url'),
                FieldPanel('linkedin_url'),
            ],
            "Social settings",
        ),
    ]

# ... keep the definition of the NavigationSettings model and add the FooterText model:
@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):
    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"