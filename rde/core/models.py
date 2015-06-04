from django.db import models
import xml.etree.ElementTree as ET
import datetime

class Supervisor(models.Model):
    surname = models.CharField(max_length = 30)
    name = models.CharField(max_length = 30)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 30)

class Bachelor(models.Model):
    authorName = models.CharField(max_length = 30)
    authorSurname = models.CharField(max_length = 30)
    authorEmail = models.EmailField()
    titlePL = models.TextField()
    titleEN = models.TextField()
    supervisor = models.ForeignKey('Supervisor')
    issueDate = models.DateField()
    abstractPL = models.TextField()
    abstractEN = models.TextField()
    keywordsPL = models.TextField()
    keywordsEN = models.TextField()
    
    def appendXML(self):
        tree = ET.parse('templates\\bachelor_template.xml');
        root = tree.getroot();
        root[2][4].text = self.authorName;
        root[2][5].text = self.authorSurname;
        root[2][6].text = self.authorEmail;
        root[3].text = self.titlePL;
        root[4].text = self.titleEN;
        root[5][0].text = self.supervisor.surname;
        root[5][1].text = self.supervisor.name;
        root[12].text = str(self.issueDate);
        root[13].text = self.abstractPL;
        root[14].text = self.abstractEN;
        root[15].text = self.keywordsPL;
        root[16].text = self.keywordsEN;
        file = open("outputBachelor.xml", mode='a')
        tree.write(file, encoding="unicode");
        file.write("\n\n");
        file.close();
        return;
    
    def generateXML(bachelors):
        for b in bachelors:
            b.appendXML();
    
class Master(models.Model):
    authorName = models.CharField(max_length = 30)
    authorSurname = models.CharField(max_length = 30)
    authorEmail = models.EmailField()
    titlePL = models.TextField()
    titleEN = models.TextField()
    supervisor = models.ForeignKey('Supervisor')
    issueDate = models.DateField()
    abstractPL = models.TextField()
    abstractEN = models.TextField()
    keywordsPL = models.TextField()
    keywordsEN = models.TextField()
    
    def appendXML(self):
        tree = ET.parse('templates\\master_template.xml');
        root = tree.getroot();
        root[2][4].text = self.authorName;
        root[2][5].text = self.authorSurname;
        root[2][6].text = self.authorEmail;
        root[3].text = self.titlePL;
        root[4].text = self.titleEN;
        root[5][0].text = self.supervisor.surname;
        root[5][1].text = self.supervisor.name;
        root[12].text = str(self.issueDate);
        root[13].text = self.abstractPL;
        root[14].text = self.abstractEN;
        root[15].text = self.keywordsPL;
        root[16].text = self.keywordsEN;
        file = open("outputMaster.xml", mode='a')
        tree.write(file, encoding="unicode");
        file.write("\n\n");
        file.close();
        return;
    
    def generateXML(masters):
        for m in masters:
            m.appendXML();