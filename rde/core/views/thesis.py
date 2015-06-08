"""
Thesis CRUD views - support rendering and validating the creation/edition form
and record deletion.
"""

from django.views.generic import View
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import ThesisForm
from ..models import Thesis as ThesisModel

class Thesis(View):
    """
    Depending on the HTTP method, either renders the creation/edition form,
    updates the thesis record or deletes it.
    """

    def get(self, request, thesis_id = None):
        """
        On GET, render edition form for the given thesis.
        If no 'thesis_id' is specified, render an empty form.
        """

        form = ThesisForm(instance = self._existing_thesis(thesis_id))
        return render(request, "thesis-form.html", {"form": form})

    def post(self, request, thesis_id = None):
        """
        On POST, validate the thesis data (provided as POST data)
        and either create/update a thesis record (if succeeded)
        or render the edition form with errors.
        """

        form = ThesisForm(request.POST, instance = self._existing_thesis(thesis_id))

        if form.is_valid():
            form.save()
            return redirect("listing")
        else:
            return render(request, "thesis-form.html", {"form": form})

    def delete(self, request, thesis_id):
        """
        On DELETE, delete the thesis record with the given thesis_id
        or return 404.
        """

        self._existing_thesis(thesis_id).delete()

    def _existing_thesis(self, thesis_id):
        """
        If thesis_id is not None, tries to return an existing Thesis object
        with this id - if it's not found, raises 404.
        If thesis_id is None, returns None.
        """

        if thesis_id is not None:
            return get_object_or_404(ThesisModel, pk = thesis_id)
        
        return None

