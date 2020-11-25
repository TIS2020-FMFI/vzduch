import datetime

from django.shortcuts import render
from django.views import View

import json
import random

from airMonitor.models.Wind import Wind


class VzduchView(View):
    def get(self, request):
        wind = Wind()
        wind_data = wind.load_data()

        return render(request, "airFinal.html", {
            "wind": wind_data
        })

    def post(self, request):
        return
