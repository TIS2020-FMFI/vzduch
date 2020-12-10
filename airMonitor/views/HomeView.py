import datetime

from django.conf import settings
from django.shortcuts import render
from django.views import View

import json
import random

from airMonitor.forms.DateForm import DateForm
from airMonitor.models.Chart import Chart
from airMonitor.models.SHMU import ObsNmsko1H, Si
from airMonitor.models.Station import Station
from airMonitor.models.AvgTable import AvgTable
from airMonitor.models.StationsTable import StationsTable
from airMonitor.services.common import add_colors

POST_DATA = None


class HomeView(View):
    def get(self, request):
        data = Chart()

        stations_table = StationsTable().load_data()

        t = AvgTable()
        table = t.load_data()
        stations = Station.all()


        if POST_DATA is not None:
            date_form = DateForm(POST_DATA)
        else:
            date_form = DateForm()

        date = datetime.datetime.now()
        if date_form.is_valid():
            date = date_form.cleaned_data.get("date")

        zl = ObsNmsko1H.objects.all().filter(date__range=[date - datetime.timedelta(days=7),
                                                          date + datetime.timedelta(days=1)])

        stations = add_colors(stations, zl.filter(date=date))

        for z in zl:
            for i in settings.ZL_LIMIT:
                data.add_data(z.si.name, i, z.__dict__[i])
            key = f"{z.date.day}.{z.date.month}.\n{str(z.date.hour).zfill(2)}:{str(z.date.minute).zfill(2)}"
            data.add_label(key)

        return render(request, "final.html", {
            "data": json.dumps(data.dict()),
            "stations": stations,
            "table": table,
            "stations_table": stations_table,
            "dateForm": date_form})

    def post(self, request):
        global POST_DATA
        date_form = DateForm(request.POST)
        # check whether it's valid:

        POST_DATA = request.POST

        return self.get(request)
