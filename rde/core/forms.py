"""
Form definitions and validation routines.
"""

from django.forms import ModelForm, RegexField, RadioSelect

from .models import Thesis

class ThesisForm(ModelForm):
    """
    Thesis record creation/modification form.
    """

    class Meta:
        model = Thesis
        exclude = ['issueYear', 'issueMonth', 'issueDay', 'supervisorLogin']
        widgets = {
            'kind': RadioSelect
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")

        if instance is not None:
            initial_issue_date = instance.issueDate()
        else:
            initial_issue_date = ""

        if "initial" in kwargs:
            kwargs["initial"].update(issueDate = initial_issue_date)
        else:
            kwargs["initial"] = {"issueDate": initial_issue_date}

        return super(ThesisForm, self).__init__(*args, **kwargs)

    def save(self, supervisor, commit = True):
        # Replace the given issueDate with a triple: issueYear, issueMonth and issueDay.
        # Set those values in the created record.

        issue_date = self.cleaned_data["issueDate"]

        for (key, value) in self._split_date(issue_date):
            setattr(self.instance, key, value)

        self.instance.supervisorLogin = supervisor

        return super(ThesisForm, self).save(commit)

    def _split_date(self, issue_date):
        year = issue_date[:4]
        month = issue_date[5:7] or None
        day = issue_date[8:10] or None

        return (("issueYear", year), ("issueMonth", month), ("issueDay", day))

    issueDate = RegexField(regex = r"^\d{4,}(-\d{2}){0,2}$")

