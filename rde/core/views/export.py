"""
Export view - supports export of selected thesis records to XML.
"""

from django.views.generic import View
from django.http import HttpResponse

from ..models import Thesis

class Export(View):
    def get(self, request):
        """
        Take a comma-separated list of thesis ids from the GET 'ids' parameter
        and generate an XML containing serialized data of the selected theses
        that will be pushed back to the browser.

        If 'ids' is not specified, a list of theses is considered to be empty
        and an empty XML is returned.
        """

        ids_string = request.GET.get("ids", "")

        # Drop all empty ids that may occur in the given string.
        # As a result, we get a list of strings that may be used to query
        # Thesis records.
        ids = filter(None, ids_string.split(","))

        theses = Thesis.objects.filter(id__in = ids)
        return HttpResponse(Thesis.generateXML(theses))

