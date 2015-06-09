"""
Helper utilities used throughout RDE.
"""

from django.shortcuts import redirect
from django.contrib import messages

from .models import Supervisor

def login_required(method):
    """
    A decorator for view methods checking if there is an authorized user
    and performing a redirect to the login form if there isn't.
    """

    def wrapped(self, request, *args, **kwargs):
        if not active_login(request):
            messages.add_message(request, messages.WARNING, "Musisz być zalogowany!")
            return redirect("login")
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

    active = active_login(request)

    if active:
        return Supervisor.objects.filter(login = active).first()

    return None

def parse_id_list(ids_string):
    """
    Splits the given comma-separated list of identifiers, returning an array.
    """

    # Drop all empty ids that may occur in the given string.
    return list(map(int, filter(None, ids_string.split(","))))

