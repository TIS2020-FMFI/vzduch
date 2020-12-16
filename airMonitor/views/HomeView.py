import datetime
import random

from django.conf import settings
from django.shortcuts import render
from django.views import View

import json

from airMonitor.forms.DateForm import DateForm
from airMonitor.models.Chart import Chart
from airMonitor.models.SHMU import ObsNmsko1H
from airMonitor.models.Station import Station
from airMonitor.models.AvgTable import AvgTable
from airMonitor.models.StationsTable import StationsTable
from airMonitor.services.common import add_colors

POST_DATA = None


class HomeView(View):
    def get(self, request):
        data = Chart()

        stations_table = StationsTable().load_data()

        stations = Station.all()

        if POST_DATA is not None:
            date_form = DateForm(POST_DATA, auto_id=False)
        else:
            date_form = DateForm(auto_id=False)

        date = datetime.datetime.now()
        if date_form.is_valid():
            date = date_form.cleaned_data.get("date") if date_form.cleaned_data.get("date") is not None else date

        zl = ObsNmsko1H.objects.all().filter(date__range=[date - datetime.timedelta(days=7),
                                                          date + datetime.timedelta(days=1)])

        stations = add_colors(stations, zl.filter(date__range=[date, date + datetime.timedelta(days=1)]))

        # ToDo dopocitat pre kazdu stanicu klzavy priemer a pridat to ako dalsiu zl s tym ze nazov bude mat avg

        for z in zl:
            for i in settings.ZL_LIMIT:
                data.add_data(z.si.name, i, z.__dict__[i])
            key = f"{z.date.day}.{z.date.month}.\n{str(z.date.hour).zfill(2)}:{str(z.date.minute).zfill(2)}"
            data.add_label(key)

        avgTable = AvgTable()
        avgTableData = avgTable.prepare_data(data.get_values("pm10")["data"])

        print(avgTableData['hours']['BRATISLAVA,JESENIOVA'])
        print(avgTableData['averages']['BRATISLAVA,JESENIOVA'])

        for station in avgTableData['hours']:
            for value in avgTableData['averages'][station]:
                data.add_data(station, "avg", value)

        d = date + datetime.timedelta(days=1)
        d = datetime.datetime(d.year, d.month, d.day)

        for i in range(5):
            d = d + datetime.timedelta(hours=1)
            key = f"{d.day}.{d.month}.\n{str(d.hour).zfill(2)}:{str(d.minute).zfill(2)}"
            data.add_label(key)

        return render(request, "final.html", {
            "data": json.dumps(data.dict()),
            "stations": stations,
            "pm_dataset": json.dumps(avgTableData),
            "stations_table": stations_table,
            "dateForm": date_form})

    def post(self, request):
        global POST_DATA
        POST_DATA = request.POST
        return self.get(request)
