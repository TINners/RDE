"""
Authorization view - supports logging users in, out and changing their passwords.
"""

from django.views.generic import View
from django.shortcuts import render

class Auth(View):
    def get(self, request):
        """
        On GET, render an empty login page.
        """

        return render(request, "login.html")

    def post(self, request):
        """
        On POST, validate the provided credentials.
        If they match, authorize the user's session and redirect
        them to the listing page.
        Otherwise render the login page with the errors highlighted.
        """

        # TODO: implement
        return render(request, "login.html")

    def delete(self, request):
        """
        On DELETE, remove user's authorization from their session
        and render the login page with a "logged out" message.
        """

        # TODO: implement
        return render(request, "login.html")

