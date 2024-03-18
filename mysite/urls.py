from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

# from wagtail.core import urls as wagtail_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


""" URLS, including both my URLS from my traditional Django views, as well as my Wagtail URLS for the pages made 
in Wagtail.

The include('blog.urls') function is used to include the URL patterns from blog/urls.py,

The URL for my traditional Django views for my blog "app" folder NEEDS TO SAY "blog/" IN THE URL. If I put literally 
anything
else in there, I won't be able to access my URLS from my views from my blog "app". Yes, this is the exact same URL
as the one for my Wagtail views for the "blog" app. However, that's how it works: both the wagtail views and the
traditional Django views for the "blog" app share the same URL. I will have to make sure that the slugs for the 
Wagtail pages and the URLS for the traditional Django views don't conflict with each other.

I will also include the "app" folder for my dashboard_app app in the URLS.
"""
urlpatterns = urlpatterns + [

    # This renders my traditional Django views from my blog "app" folder. IT NEEDS TO SAY "blog/" IN THE URL.
    path('blog/', include('blog.urls')),

    # This renders my traditional Django views from my dashboard_app app folder. IT NEEDS TO SAY "dashboard_app/" IN THE URL.
    path('dashboard_app/', include('dashboard_app.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
