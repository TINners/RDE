"""
Authorization view - supports logging users in, out and changing their passwords.
"""

from django.views.generic import View
from django.shortcuts import render
import xml.etree.ElementTree as ET


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
        """
        # to improve
        fileName = 'users.xml'
        l = request.POST['login']
        p = request.POST['password']
        tree = ET.parse(fileName);
        root = tree.getroot();
        index = getUserIndexByLogin(l, root)
        
        if index == -1:
            # write niepoprawny login
            return render(request, "login.html")          # blad autoryzacji, niepoprawny login
            
        if root[index][1].text != None:                       # Jest password w bazie
            if(root[index][1].text != p):
                # write niepoprawne haslo                 # password nie zgadza sie
                return render(request, "login.html")      # blad autoryzacji
                
        elif p != None and p != '':                       # podal haslo
            updatePassword(index, p, tree, fileName)      # update hasla
       
        request.session['login'] = l
        return render(request, "listing.html")
        
            
    def delete(self, request):
        """
        On DELETE, remove user's authorization from their session
        and render the login page with a "logged out" message.
        """
        
        # to improve. Need to write "logged out"
        request.session['login'] = None
        return render(request, "login.html")
        
        
    def getUserIndexByLogin(l, root):
        i = 0
        for r in root:
            if(r[0].text == l):
                return i
            i = i + 1
        
        return -1
        
        
    def updatePassword(index, password, tree, fileName):
        root = tree.getroot()
        root[index][1].text = password
        file = open(fileName, mode='w')
        tree.write(file, encoding="unicode")
        file.close()
        return