from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

import xml.etree.ElementTree as ET

from datetime import date

class Supervisor(models.Model):
    """
    Represents a supervisor's template.
    If such a record is present for the currently authorized supervisor,
    data specified here will be automatically input when adding a thesis.
    """

    email = models.EmailField(unique = True, primary_key = True)
    surname = models.CharField(max_length = 30, null = True, default = None)
    name = models.CharField(max_length = 30, null = True, default = None)

class Thesis(models.Model):
    """
    Represents a thesis - either a bachelor or master one.
    """

    def clean(self):
        """
        Validate correctness of the whole record.
        """

        self.validate_date(self.issueYear, self.issueMonth, self.issueDay)

    @staticmethod
    def validate_month(value):
        """
        Validate a month - it must be between 1 and 12.
        """

        if value < 1 or value > 12:
            raise ValidationError("{} is not a valid month number!".format(value))

    @staticmethod
    def validate_day(value):
        """
        Validate a day - it must be between 1 and 31.
        """

        if value < 1 or value > 12:
            raise ValidationError("{} is not a valid month number!".format(value))

    @staticmethod
    def validate_date(year, month, day):
        """
        Validate the given date - is the given day of the month valid?
        """

        if day is None:
            # If day is not given, the date is valid at this point.
            return

        try:
            date(year = year, month = month, day = day)
        except ValueError:
            raise ValidationError("{year}-{month}-{day} is not a valid date!".format(
                year = year, month = month, day = day))

    def issueDate(self):
        """
        Return an issue date as a string.
        """

        year = str(self.issueYear)
        month = ("-%02d" % self.issueMonth) if self.issueMonth else ""
        day = ("-%02d" % self.issueDay) if self.issueDay else ""

        return year + month + day

    def _XMLtemplate(self):
        """
        Return a path to the proper XML template for this kind of thesis.
        """

        return "templates/{kind}_template.xml".format(
            kind = "bachelor" if self.kind == "B" else "master")
    
    def asXML(self):
        """
        Serialize this thesis record to XML using a proper template.
        """

        tree = ET.parse(_XMLtemplate());
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
    
        return root.tostring(encoding = 'unicode')

    @classmethod
    def generateXML(cls, theses):
        """
        Generate an XML for the given set of thesis records.

        Attention: all the records must be of the same kind!
        (that is: it's illegal to mix bachelor and master records).
        """

        assert len(theses)
        assert all(t.kind == theses[0].kind for t in theses)

        "\n".join(t.asXML() for t in theses)

    # A regular expression for validating keyword fields
    _keywords_regex = r"^[\w -]+(,( ?)\w[\w -]+)*$"

    # Kind of this thesis - bachelor or master.
    kind = models.CharField(
        max_length = 1,
        choices = (
            ("B", "Praca inżynierska"),
            ("M", "Praca magisterska")))

    authorName = models.CharField(max_length = 30)
    authorSurname = models.CharField(max_length = 30)
    authorEmail = models.EmailField()

    titlePL = models.TextField()
    titleEN = models.TextField()

    # Issue year must be specified. Month and day are optional.
    issueYear = models.PositiveIntegerField()
    issueMonth = models.PositiveSmallIntegerField(
        null = True,
        default = None,
        validators = [validate_month])
    issueDay = models.PositiveSmallIntegerField(
        null = True,
        default = None,
        validators = [validate_day])

    abstractPL = models.TextField()
    abstractEN = models.TextField()

    # Keywords are required to be comma-separated alphanumeric strings.
    keywordsPL = models.TextField(
        validators = [RegexValidator(_keywords_regex)])
    keywordsEN = models.TextField(
        validators = [RegexValidator(_keywords_regex)])

    supervisorName = models.CharField(max_length = 30)
    supervisorSurname = models.CharField(max_length = 30)


