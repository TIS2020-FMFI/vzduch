class AvgTable:
    def __init__(self):
        self._moving_average = {'12h': dict(), '24h': dict()}

    def prepare_data(self, data):
        """ counts moving average from hour values of PM_10
            returns an object with hour values and corresponding moving average
        """
        for key in data:
            arr_len = len(data[key])
            self._moving_average['12h'][key] = []
            self._moving_average['24h'][key] = []
            k = 0
            for i in range(12, arr_len+1):
                self._moving_average['12h'][key].append(self.average(data[key][k:i], 12))
            for i in range(24, arr_len + 1):
                self._moving_average['24h'][key].append(self.average(data[key][k:i], 24))
                k += 1

            if len(self._moving_average['12h'][key]) < 168:
                self._moving_average['12h'][key] = [None]*12 + self._moving_average['12h'][key]

        return {'hours': data, 'moving_average': self._moving_average}

    def average(self, hour_values, hours):
        """counts average from input values"""
        sum = 0
        for i in hour_values:
            if i is not None:
                sum += i
        ret = round(sum / hours, 1)
        return ret if ret != 0 else None
