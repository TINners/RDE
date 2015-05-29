"""
Root URL config.
"""

from django.conf.urls import url, include

from core.urls import urlpatterns as core_urls

urlpatterns = [
    url(r'', include(core_urls))
]

