import datetime

from django.shortcuts import render
from django.views import View

import json
import random

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

        t = AvgTable()
        table = t.load_data()
        # print(table)

        date_list = ["NO2", "PM10", "PM2,5", "O3"]
        s = ObsNmsko1H.objects.all()

        stations = Station.all()

        if POST_DATA is not None:
            date_form = DateForm(POST_DATA)
        else:
            date_form = DateForm()

        date = datetime.datetime.now()
        if date_form.is_valid():
            date = date_form.cleaned_data.get("date")

        for i in range(len(stations)):
            stations[i].set_color("red", "#f03")

        print(len(s))

        for date in date_list:
            for i in range(10):
                data.add_data(str(date), random.random() * 5)
                data.add_label(f"hour{i + 1}")

        #print(json.dumps(data.dict(), indent=4))

        return render(request, "final.html", {
            "data": json.dumps(data.dict()),
            "stations": stations,
            "table": table,
            "stations_table": stations_table,
            "dateForm": date_form})


    def post(self, request):

        return