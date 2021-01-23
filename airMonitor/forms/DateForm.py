from django import forms
from django.forms import Form

from airMonitor.models.SHMU import ObsNmsko1H

YEARS = set(range(2018, 2030))
#set(x.year for x in ObsNmsko1H.objects.values_list('date', flat=True))


class DateForm(Form):
    date = forms.DateField(label="", widget=forms.SelectDateWidget(years=YEARS), required=False)

    class Meta:
        pass

