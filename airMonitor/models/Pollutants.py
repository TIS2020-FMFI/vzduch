import pandas as pd

from airMonitor.services.database import Database


class Pollutant:

    @staticmethod
    def all(from_date, to_date, stations_id):
        result = dict()
        connection = Database.get_connection()
        data = pd.read_sql_query(f"SELECT * FROM si.obs_nmsko_1h WHERE si.obs_nmsko_1h.date >= {from_date} and si.obs_nmsko_1h.date <= {to_date}" +
                                           f" and si.obs_nmsko_1h.si_id in ({', '.join(stations_id)})", connection)
        for pollutant in data:
            print(pollutant)
            # result.append(Station(station.name))
        return result

    def __init__(self, data):
        self.obs_id = None
        self.si = None
        self.date = None
        self.ta_2m = None
        self.pa_avg = None
        self.rh_avg = None
        self.ws_avg = None
        self.wd_avg = None
        self.ws_max = None
        self.wd_ws_max = None
        self.pr_sum = None
        self.hg = None
        self.pm10 = None
        self.pm2_5 = None
        self.so2 = None
        self.no = None
        self.no2 = None
        self.nox = None
        self.co = None
        self.ben = None
        self.h2s = None
        self.o3 = None

