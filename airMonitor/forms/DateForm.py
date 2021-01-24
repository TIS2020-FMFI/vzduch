from django import forms
from django.forms import Form

YEARS = list(range(2010, 2050))


class DateForm(Form):
    date = forms.DateField(label="", widget=forms.SelectDateWidget(years=YEARS), required=False)

    class Meta:
        pass

