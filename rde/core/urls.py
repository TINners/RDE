"""
Core URLs.
"""

from django.conf.urls import url

from .views import (
    Auth,
    Listing,
    Thesis,
    Settings,
    Export
)

urlpatterns = [
    url(r'^login/$', Auth.as_view(), name = "login"),
    url(r'^settings/$', Settings.as_view(), name = "settings"),

    url(r'^export/$', Export.as_view(), name = "export"),

    url(r'^$', Listing.as_view(), name = "listing"),
    url(r'^thesis/create/$', Thesis.as_view(), name = "thesis-create"),
    url(r'^thesis/(?P<thesis_id>.+)/$', Thesis.as_view(), name = "thesis-update-delete"),
]

