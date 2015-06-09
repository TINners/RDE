"""
Thesis CRUD views - support rendering and validating the creation/edition form
and record deletion.
"""

from django.views.generic import View
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseBadRequest, Http404

from ..forms import ThesisForm
from ..models import Thesis as ThesisModel
from ..helpers import login_required, active_login, active_template, parse_id_list

class Thesis(View):
    """
    Depending on the HTTP method, either renders the creation/edition form,
    updates the thesis record or deletes it.
    """

    @login_required
    def get(self, request, thesis_id = None):
        """
        On GET, render edition form for the given thesis.
        If no 'thesis_id' is specified, render an empty form.
        """

        form = ThesisForm(instance = self._existing_thesis(thesis_id))
        editing = thesis_id is not None

        return render(request, "thesis-form.html", {
            "form": form,
            "submit_to": self._submit_url(thesis_id),
            "editing": editing
        })

    @login_required
    def post(self, request, thesis_id = None):
        """
        On POST, validate the thesis data (provided as POST data)
        and either create/update a thesis record (if succeeded)
        or render the edition form with errors.
        """

        form = ThesisForm(request.POST, instance = self._existing_thesis(thesis_id))
        editing = thesis_id is not None

        if form.is_valid():
            form.save(supervisor = active_login(request))

            if not editing:
                success_msg = "Dodano pracę {}!".format(
                    "inżynierską" if form.cleaned_data['kind'] == "B" else "magisterską")
            else:
                success_msg = "Zapisano zmiany!"

            messages.add_message(request, messages.SUCCESS, success_msg)

            return redirect("listing")
        else:
            return render(request, "thesis-form.html", {
                "form": form,
                "submit_to": self._submit_url(thesis_id),
                "editing": editing
            })

    def _existing_thesis(self, thesis_id):
        """
        If thesis_id is not None, tries to return an existing Thesis object
        with this id - if it's not found, raises 404.
        If thesis_id is None, returns None.
        """

        if thesis_id is not None:
            return get_object_or_404(
                ThesisModel,
                pk = thesis_id,
                supervisorLogin = active_login(request))

        return None

    def _submit_url(self, thesis_id):
        """
        Returns an URL the creation/edition form should be submitted to.
        """

        if thesis_id is None:
            return reverse("thesis-create")
        else:
            return reverse("thesis-update", kwargs = {"thesis_id": thesis_id})

class ThesisDelete(View):
    @login_required
    def post(self, request):
        """
        On POST, delete the thesis records with the ids given as POST data.

        If "ids" is missing from POST, raise 400.
        """

        ids = parse_id_list(request.POST.get("ids", ""))

        if not ids:
            return HttpResponseBadRequest("'ids' must be provided!")

        theses = ThesisModel.objects.filter(
            id__in = ids,
            supervisorLogin = active_login(request))
        for t in theses:
            t.delete()

        success_msg = ("Usunięto pracę!"
            if len(theses) == 1
            else "Usunieto {} prac!".format(len(theses)))

        messages.add_message(request, messages.SUCCESS, success_msg)
        return redirect("listing")

