import json

from airMonitor.models.SHMU import Si

from django.db.models import Q


class Station:

    @staticmethod
    def all():
        result = []
        for station in Si.objects.filter(ci=78).filter(~Q(lat=0.0)):
            result.append(Station(station.name))
        return result

    def __init__(self, name, color_name=None, color_code=None, zl=None):
        self._station = Si.objects.all().filter(name=name).first()
        self._id = self._station.id
        self.color_name = color_name
        self.color_code = color_code
        self.zl = zl

    def set_color(self, color_name, color_code):
        self.color_name = color_name
        self.color_code = color_code

    def set_zl(self, zl):
        self.zl = zl

    def get_station(self):
        return self._station

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps({
            "name": self._station.name,
            "id": self._id,
            "lat": self._station.lat,
            "lon": self._station.lon,
            "zl": self.zl,
            "color_name": self.color_name,
            "color_code": self.color_code

        }, indent=4)
