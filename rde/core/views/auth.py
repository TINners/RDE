"""
Authorization view - supports logging users in, out and changing their passwords.
"""

from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib import messages

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from ..helpers import login_required

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

        Attention: if there is no password set for the user and one
        is provided in the form, user's password is updated!
        """

        login = request.POST.get("login")
        password = request.POST.get("password")

        if not login:
            return render(request, "login.html", {"error": True})

        (login_correct, correct_password) = self._user_credentials(login)

        if not login_correct:
            # Invalid login.
            return self._render_with_error(request)
        elif correct_password and correct_password != password:
            # There is a password in the configuration, but it doesn't match.
            return self._render_with_error(request)
        elif not correct_password and password:
            # There is no password in the configuration, but the user has provided
            # one, so set it and notify the user.
            self._create_password(login, password)
            messages.add_message(request, messages.INFO, "Hasło zostało ustawione!")

        request.session["login"] = login

        return redirect("listing")

    def _render_with_error(self, request):
        """
        Render the login form with an error message.
        """

        return render(request, "login.html", {"error": True})

    def _user_credentials(self, login):
        """
        Retrieve credentials for the given login.
        Returns a tuple: (is the user registered?, user's password).

        Attention: user's password will be None if unset.
        """

        tree = self._users_xml()
        user_element = tree.find('user[l="{}"]'.format(login))

        if user_element is None:
            return (False, None)
        else:
            password = user_element.findtext("p")
            return (True, password or None)

    def _create_password(self, login, password):
        """
        Creates a password for the given user.
        """

        tree = self._users_xml()
        user_element = tree.find('user[l="{}"]'.format(login))

        existing_pwd_element = user_element.find("p")
        if existing_pwd_element:
            user_element.remove(existing_pwd_element)

        pwd_element = ET.SubElement(user_element, "p")
        pwd_element.text = password

        with open(self._users_xml_path, 'w') as f:
            tree.write(f, encoding="unicode")

    def _users_xml(self):
        """
        Returns an XML tree of the users' configuration file.
        """

        return ET.parse(self._users_xml_path)

    _users_xml_path = "config/users.xml"

class Logout(View):
    """
    Logs the user out on GET.
    """

    @login_required
    def get(self, request):
        """
        On GET, remove the user's authorization from their session
        and render the login page with a "logged out" message.
        """

        del request.session["login"]

        messages.add_message(request, messages.INFO, "Wylogowano!")
        return redirect("login")

