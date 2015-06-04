from django.utils import timezone
from core.models import *

def generateBachelor(supervisor):
    b = Bachelor()
    b.authorName = "Roman"
    b.authorSurname = "Kowalski"
    b.authorEmail = "adres@poczta.pl"
    b.titlePL = "Jakis tytul"
    b.titleEN = "A title"
    b.supervisor = supervisor
    b.issueDate = timezone.now()
    b.abstractPL = "Jakis dluzszu text"
    b.abstractEN = "Something very long"
    b.keywordsPL = "Jeden, dwa, trzy"
    b.keywordsEN = "One, two, three"
    return b;
    
def generateMaster(supervisor):
    b = Master()
    b.authorName = "Stefan"
    b.authorSurname = "Rybicki"
    b.authorEmail = "adres12@poczta.pl"
    b.titlePL = "Jakis tytul1"
    b.titleEN = "A title1"
    b.supervisor = supervisor
    b.issueDate = timezone.now()
    b.abstractPL = "Jakis dluzszu text"
    b.abstractEN = "Something very long"
    b.keywordsPL = "Jeden, dwa, trzy"
    b.keywordsEN = "One, two, three"
    return b;

    
def generateSupervisor():
    s = Supervisor()
    s.surname = "Andrzej"
    s.name = "Nowak"
    s.email = "email@skrzynka.com"
    s.password = "123456"
    return s;