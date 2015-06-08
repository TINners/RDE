"""
Listing view - supports rendering the theses listing page.
"""

from django.views.generic import View
from django.shortcuts import render

from ..models import Thesis
from ..helpers import login_required

class Listing(View):
    @login_required
    def get(self, request):
        """
        On GET, render a listing of all thesis records assigned
        to the active account.
        """

        all_theses = Thesis.objects.all

        return render(request, "listing.html", {"theses": all_theses})

