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


""" This is the FormPage model. It inherits from AbstractEmailForm, which is a Wagtail model that represents a page
that has a form. The FormPage model has an intro field, which is a RichTextField. The intro field is a rich text field
that I can use to add a description to the form. The thank_you_text field is also a RichTextField. It's the text that
will be displayed to the user after they submit the form. The get_form method is a method that I can override to
customize the form. In this case, I'm adding a class to each field in the form. The content_panels attribute is a list
of panels that I can use to customize the form in the Wagtail Admin panel. The FormSubmissionsPanel is a panel that
displays the form submissions in the Wagtail Admin panel. The FieldPanel is a panel that I can use to customize the
fields in the form. The InlinePanel is a panel that I can use to customize the form fields. The MultiFieldPanel is a
panel that I can use to group other panels. 

This is the equivalent of a forms.py file in a traditional Django app. It's where I define the form that I want to
display on the page.

To add a class to each field in the form, you can override the get_form method in your form model. The get_form method 
is called to get the form instance. You can add the classes to the form fields in this method. This code will render 
each form field with the form-control class.

You can add placeholder text to each field in the form by modifying the get_form method in your form model. In this 
method, you can add a placeholder attribute to each field's widget. The placeholder text is defined in the placeholders 
dictionary. You can add more fields to this dictionary if you have more fields in your form. The "get_form" code will 
render each form field with the form-control class and the appropriate placeholder text.
"""


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    # This adds a class to each field in the form to render each form field with the "form-control" class.
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # This will only add placeholder text to the name, email, and message fields in the form.
        placeholders = {
            'name': 'Your name',
            'email': 'Your email',
            'message': 'Your message',
        }
        # Add a class and placeholder text to each field in the form
        # for field in form.fields.values():
        #     field.widget.attrs['class'] = 'form-control'
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # This adds a "placeholder" value to the field if the field name is in the placeholders dictionary.
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]
        return form

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