"""
Helper utilities used throughout RDE.
"""

from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .models import Supervisor

def login_required(method):
    """
    A decorator for view methods checking if there is an authorized user
    and performing a redirect to the login form if there isn't.
    """

    def wrapped(self, request, *args, **kwargs):
        if not active_login(request):
            return redirect(reverse("login") + "?message=Musisz być zalogowany!")
        else:
            return method(self, request, *args, **kwargs)

    return wrapped

def active_login(request):
    """
    Returns an e-mail of the currently authorized user or None if there's none.
    """

    return request.session.get("login")

def active_template(request):
    """
    Returns a Supervisor object (if there's any) of the currently authorized user.
    """

    if active_login():
        return Supervisor.objects.filter(pk = active_login()).get(0) or None

    return None

