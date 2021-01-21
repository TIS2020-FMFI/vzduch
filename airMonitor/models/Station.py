import json

import pandas as pd

from airMonitor.services.database import Database


class Station:

    @staticmethod
    def all():
        result = dict()
        connection = Database.get_connection()
        for station in pd.read_sql_query("SELECT * FROM si WHERE ci = 78", connection):
            print(station)
            #result.append(Station(station.name))
        return result

    class Si:
        def __init__(self, data):
            self.id = None
            self.ci = None
            self.ii = None
            self.name = None
            self.cccc = None
            self.cc = None
            self.iso_cc = None
            self.lat = None
            self.lon = None
            self.elev = None
            self.info = None
            self.vtime = None
            self.mtime = None
            self.changed_id = None
            self.changes = None
            self.ue = None

    def __init__(self, data, color_name=None, color_code=None, zl=None):

        self.station = self.Si(data)
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
