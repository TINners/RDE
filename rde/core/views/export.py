"""
Export view - supports export of selected thesis records to XML.
"""

from django.views.generic import View
from django.http import HttpResponse

from ..models import Thesis
from ..helpers import parse_id_list, active_login

class Export(View):
    def post(self, request):
        """
        Take a comma-separated list of thesis ids from the GET 'ids' parameter
        and generate an XML containing serialized data of the selected theses
        that will be pushed back to the browser.

        If 'ids' is not specified, a list of theses is considered to be empty
        and an empty XML is returned.
        """

        ids = parse_id_list(request.POST.get("ids", ""))

        theses = Thesis.objects.filter(
            id__in = ids,
            supervisorLogin = active_login(request))

        return HttpResponse(Thesis.generateXML(theses),
            content_type = "text/plain")

