from django.db import models

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