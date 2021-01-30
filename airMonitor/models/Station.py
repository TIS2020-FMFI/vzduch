import json

import pandas as pd

from airMonitor.services.database import Database


class Station:
    stations = []
    @staticmethod
    def all():
        if len(Station.stations) != 0:
            return Station.stations
        result = list()
        sql = "SELECT * FROM si.si WHERE ci = 78"
        data = Database.execute_sql(sql)
        for station in data.itertuples():
            result.append(Station(Station.Si(station)))
        Station.stations = result
        return result

    class Si:
        def __init__(self, data):
            self.id = data[1]
            self.ci = data[2]
            self.ii = data[3]
            self.name = data[4]
            self.cccc = data[5]
            self.cc = data[6]
            self.iso_cc = data[7]
            self.lat = data[8]
            self.lon = data[9]
            self.elev = data[10]
            self.info = data[11]
            self.vtime = data[12]
            self.mtime = data[13]
            self.changed_id = data[14]
            self.changes = data[15]
            self.ue = data[16]

        def __str__(self):
            return self.name

    def __init__(self, si, color_name=None, color_code=None, zl=None):

        self.station = si
        self.color_name = color_name
        self.color_code = color_code
        self.zl = zl

    def set_color(self, color_name, color_code):
        self.color_name = color_name
        self.color_code = color_code

    def set_zl(self, zl):
        self.zl = zl

    def get_station(self):
        return self.station

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps({
            "name": self.station.name,
            "lat": self.station.lat,
            "lon": self.station.lon,
            "zl": self.zl,
            "color_name": self.color_name,
            "color_code": self.color_code

        }, indent=4)
