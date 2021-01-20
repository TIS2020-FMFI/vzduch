import datetime
import json
import logging

from django.conf import settings
from django.shortcuts import render
from django.views import View



from airMonitor.forms.DateForm import DateForm
from airMonitor.models.Chart import Chart
from airMonitor.models.SHMU import ObsNmsko1H
from airMonitor.models.Station import Station
from airMonitor.models.AvgTable import AvgTable
from airMonitor.models.StationsTable import StationsTable
from airMonitor.services.common import add_colors

POST_DATA = None

logger = logging.getLogger("django")


class HomeView(View):
    def get(self, request):
        if POST_DATA is not None:
            date_form = DateForm(POST_DATA, auto_id=False)
        else:
            date_form = DateForm(auto_id=False)

        date = datetime.datetime.now()
        if date_form.is_valid():
            date = date_form.cleaned_data.get("date") if date_form.cleaned_data.get("date") is not None else date

        data = Chart()

        stations_table = StationsTable().load_data(date)

        stations = Station.all()

        zl = ObsNmsko1H.objects.all().filter(date__range=[date - datetime.timedelta(days=7),
                                                          date + datetime.timedelta(days=1)]).order_by("date")

        stations = add_colors(stations, zl.filter(date__range=[date, date + datetime.timedelta(days=1)]))

        for z in zl:
            key = f"{z.date.day}.{z.date.month}.\n{str(z.date.hour).zfill(2)}:{str(z.date.minute).zfill(2)}"
            for i in settings.POLLUTANTS:
                data.add_data(station=z.si.name, pollutant=i, data=z.__dict__[i], date=key)

        avg_table_data = dict()
        try:
            avg_table = AvgTable()
            avg_table_data = avg_table.prepare_data(data.get_values("pm10")["data"])
            for station in avg_table_data['hours']:
                for value in avg_table_data['averages'][station]:
                    data.add_data(station=station, pollutant="avg", data=value, date=None)
        except Exception as ex:
            logger.error(ex)

        try:
            data.normalize_data()
        except KeyError as ex:
            logger.error("No pollutant named " + ex.args[0])
        data.add_colors()

        data.get_maximal_values("2")

        d = date + datetime.timedelta(days=1)
        d = datetime.datetime(d.year, d.month, d.day)

        for i in range(5):
            d = d + datetime.timedelta(hours=1)
            key = f"{d.day}.{d.month}.\n{str(d.hour).zfill(2)}:{str(d.minute).zfill(2)}"
            data.add_label(key)

        return render(request, "final.html", {
            "data": json.dumps(data.dict()),
            "stations": stations,
            "pm_dataset": json.dumps(avg_table_data),
            "stations_table": stations_table,
            "dateForm": date_form})

    def post(self, request):
        global POST_DATA
        POST_DATA = request.POST
        return self.get(request)
