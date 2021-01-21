import pandas as pd

from airMonitor.services.database import Database


class Pollutant:

    @staticmethod
    def all(from_date, to_date, stations_id):
        result = list()
        try:
            from_date = from_date.date()
            to_date = to_date.date()
        except:
            pass
        connection = Database.get_connection()
        data = pd.read_sql_query(f"SELECT * FROM obs.obs_nmsko_1h WHERE obs.obs_nmsko_1h.date >= {from_date} and obs.obs_nmsko_1h.date <= {to_date}" +
                                 f" and obs.obs_nmsko_1h.si_id in ({', '.join([str(x) for x  in stations_id])})", connection)
        for pollutant in data.itertuples():
            result.append(Pollutant(pollutant))
        return result

    def __init__(self, data):
        self.obs_id = data[1]
        self.si = data[2]
        self.date = data[3]
        self.ta_2m = data[4]
        self.pa_avg = data[5]
        self.rh_avg = data[6]
        self.ws_avg = data[7]
        self.wd_avg = data[8]
        self.ws_max = data[9]
        self.wd_ws_max = data[10]
        self.pr_sum = data[11]
        self.hg = data[12]
        self.pm10 = data[13]
        self.pm2_5 = data[14]
        self.so2 = data[15]
        self.no = data[16]
        self.no2 = data[17]
        self.nox = data[18]
        self.co = data[19]
        self.ben = data[20]
        self.h2s = data[21]
        self.o3 = data[22]
