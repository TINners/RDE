"""
Thesis CRUD views - support rendering and validating the creation/edition form
and record deletion.
"""

from django.views.generic import View

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

        # TODO

    def post(self, request, thesis_id = None):
        """
        On POST, validate the thesis data (provided as POST data)
        and either create/update a thesis record (if succeeded)
        or render the edition form with errors.
        """

        # TODO

    def delete(self, request, thesis_id):
        """
        On DELETE, delete the thesis record with the given thesis_id
        or return 404.
        """

        # TODO

