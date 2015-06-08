"""
Authorization view - supports logging users in, out and changing their passwords.
"""

from django.views.generic import View
from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET

from ..helpers import login_required

class Auth(View):
    def get(self, request):
        """
        On GET, render an empty login page.
        """

        message = request.GET.get("message")
        return render(request, "login.html", {"message": message})

    def post(self, request):
        """
        On POST, validate the provided credentials.
        If they match, authorize the user's session and redirect
        them to the listing page.
        Otherwise render the login page with the errors highlighted.
        """
        # to improve
        file_name = 'users.xml'
        l = request.POST['login']
        p = request.POST['password']
        tree = ET.parse(file_name);
        root = tree.getroot();
        index = self._user_index_by_login(l, root)

        if index == -1:
            # blad autoryzacji, niepoprawny login
            return render(request, "login.html", {"error": True})

        # Jest password w bazie
        pwd_in_file = root[index].get(1)
        if pwd_in_file and pwd_in_file.text:
            if pwd_in_file.text != p:
                # niepoprawne hasło
                return render(request, "login.html", {"error": True})

        # Nie ma hasła w bazie, ale użytkownik je podał:
        elif p:
            self._update_password(index, p, tree, file_name)

        request.session['login'] = l

        return redirect("listing")

    @login_required
    def delete(self, request):
        """
        On DELETE, remove user's authorization from their session
        and render the login page with a "logged out" message.
        """

        # to improve. Need to write "logged out"
        request.session['login'] = None
        return render(request, "login.html")

    def _user_index_by_login(self, l, root):
        i = 0
        for r in root:
            if(r[0].text == l):
                return i
            i = i + 1

        return -1

    def _update_password(self, index, password, tree, fileName):
        root = tree.getroot()
        root[index][1].text = password
        file = open(fileName, mode='w')
        tree.write(file, encoding="unicode")
        file.close()

