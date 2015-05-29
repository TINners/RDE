"""
Settings view - supports displaying and altering user's settings.
"""

from django.views.generic import View
from django.shortcuts import render

class Settings(View):
    def get(self, request):
        """
        On GET, render the settings form for the active user.
        """

        # TODO

        return render(request, "settings.html")

    def post(self, request):
        """
        On POST, validate and update the active user's settings.
        """

        # TODO

