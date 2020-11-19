import datetime

from django.shortcuts import render
from django.views import View

import json
import random

from airMonitor.models.Chart import Chart
from airMonitor.models.SHMU import ObsNmsko1H
from airMonitor.models.Station import Station
from airMonitor.models.AvgTable import AvgTable


class VzduchView(View):
    def get(self, request):

        return


    def post(self, request):
        return