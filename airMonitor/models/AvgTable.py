from airMonitor.models.SHMU import ObsNmsko1H, Si
from airMonitor.models.Station import Station


class AvgTable:
    def __init__(self):
        self._hour_vals = dict() # {key<station.id>: value<list of last 24h meterings>
        self._moving_avg_vals = dict()

    def load_data(self):
        vals = ObsNmsko1H.objects.all()
        stations_id = Si.objects.values_list('id', flat=True)
        self._hour_vals['stations'] = list(stations_id)

        for id in stations_id:
            self._hour_vals[id] = list(map(lambda x: round(x, 2) if type(x) == float else x,
                vals.filter(si_id=id).order_by('-date')[:25].values_list('pm10', flat=True)))

            avg_vals = []
            for i in range(13):
                avg_vals.append(self.moving_average(self._hour_vals[id][i:i+12]))

            self._moving_avg_vals[id] = avg_vals

        return {'hours': self._hour_vals, 'averages': self._moving_avg_vals}

    def moving_average(self, hour_values):
        sum = 0
        for i in hour_values:
            if i is not None:
                sum += i

        return round(sum/12, 2)






