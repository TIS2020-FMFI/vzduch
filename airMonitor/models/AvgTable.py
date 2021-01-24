class AvgTable:
    def __init__(self):
        self._avg_vals = dict()

    def prepare_data(self, data):
        """ counts moving average from hour values of PM_10
            returns an object with hour values and corresponding moving average
        """
        for key in data:
            arr_len = len(data[key])
            self._avg_vals[key] = []
            k = 0
            for i in range(12, arr_len+1):
                self._avg_vals[key].append(self.average(data[key][k:i]))
                k += 1

            if len(self._avg_vals[key]) < 168:
                self._avg_vals[key] = [None]*12 + self._avg_vals[key]

        return {'hours': data, 'averages': self._avg_vals}

    def average(self, hour_values):
        """counts average from input values"""
        sum = 0
        for i in hour_values:
            if i is not None:
                sum += i
        ret = round(sum / 12, 1)
        return ret if ret != 0 else None
