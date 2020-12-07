from django import forms
from django.forms import ModelForm, Form
from django.utils.translation import gettext_lazy as _
from django.utils.dates import MONTHS as M


from airMonitor.models.SHMU import ObsNmsko1H
from airMonitor.models.Station import Station

YEARS = set([x.year for x in ObsNmsko1H.objects.values_list('date', flat=True)])
MONTHS = {x: M[x] for x in M if x in set([x.month for x in ObsNmsko1H.objects.values_list('date', flat=True)])}
STATIONS = [(x.get_station().id, x.get_station().name) for x in Station.all()]


class DateForm(Form):
    date = forms.DateField(label='Datum', widget=forms.SelectDateWidget(years=YEARS, months=MONTHS), required=False)
    days = forms.ChoiceField(choices=[(str(x), str(x)) for x in range(1, 8)], required=False)
    stations = forms.ChoiceField(choices=STATIONS, required=False)

    class Meta:
        pass

