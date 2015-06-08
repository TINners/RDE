"""
Core URLs.
"""

from django.conf.urls import url

from .views import (
    Auth,
    Logout,
    Listing,
    Thesis,
    Export
)

urlpatterns = [
    url(r'^login/$', Auth.as_view(), name = "login"),
    url(r'^logout/$', Logout.as_view(), name = "logout"),

    url(r'^export/$', Export.as_view(), name = "export"),

    url(r'^$', Listing.as_view(), name = "listing"),
    url(r'^thesis/create/$', Thesis.as_view(), name = "thesis-create"),
    url(r'^thesis/(?P<thesis_id>.+)/$', Thesis.as_view(), name = "thesis-update-delete"),
]

