import datetime

from django.shortcuts import render
from django.views import View

import json
import random

from airMonitor.models.Chart import Chart
from airMonitor.models.SHMU import ObsNmsko1H
from airMonitor.models.Station import Station
from airMonitor.models.AvgTable import AvgTable

class AirMonitorView(View):
    def get(self, request):
        data = Chart()

        t = AvgTable()
        table = t.load_data()
        # print(table)

        date_list = ["NO2", "PM10", "PM2,5", "O3"]
        s = ObsNmsko1H.objects.all()

        stations = Station.objects.all()

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
            "table": table})


    def post(self, request):

        return