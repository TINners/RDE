"""
Listing view - supports rendering the theses listing page.
"""

from django.views.generic import View
from django.shortcuts import render

class Listing(View):
    def get(self, request):
        """
        On GET, render a listing of all thesis records assigned
        to the active account.
        """

        # TODO

        return render(request, "listing.html")

