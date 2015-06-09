from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

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

        return "config/{kind}_template.xml".format(
            kind = "bachelor" if self.kind == "B" else "master")

    def asXML(self):
        """
        Serialize this thesis record to XML using a proper template.
        """

        with open(self._XMLtemplate()) as f:
            template = f.read()

        return template.format(
            authorName = self.authorName,
            authorSurname = self.authorSurname,
            authorEmail = self.authorEmail,
            titlePL = self.titlePL,
            titleEN = self.titleEN,
            supervisorName = self.supervisorName,
            supervisorSurname = self.supervisorSurname,
            issueDate = self.issueDate(),
            abstractPL = self.abstractPL,
            abstractEN = self.abstractEN,
            keywordsPL = self.keywordsPL,
            keywordsEN = self.keywordsEN)

    @classmethod
    def generateXML(cls, theses):
        """
        Generate an XML for the given set of thesis records.

        Attention: all the records must be of the same kind!
        (that is: it's illegal to mix bachelor and master records).
        """

        assert len(theses)
        assert all(t.kind == theses[0].kind for t in theses)

        return "\n".join(t.asXML() for t in theses)

    # A regular expression for validating keyword fields
    _keywords_regex = r"^[\w -]+(,( ?)\w[\w -]+)*$"

    # Kind of this thesis - bachelor or master.
    kind = models.CharField(
        max_length = 1,
        choices = (
            ("B", "Praca inżynierska"),
            ("M", "Praca magisterska")),
        default = "B")

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

    supervisorLogin = models.EmailField()
    supervisorName = models.CharField(max_length = 30)
    supervisorSurname = models.CharField(max_length = 30)

