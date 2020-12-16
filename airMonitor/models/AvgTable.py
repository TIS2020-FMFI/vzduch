class AvgTable:
    def __init__(self):
        self._avg_vals = dict()

    """ 
    counts moving average from hour values of PM_10
    returns an object with hour values and corresponding moving average 
    """

    def prepare_data(self, data):
        for key in data:
            arr_len = len(data[key])
            self._avg_vals[key] = []
            k = 0
            for i in range(arr_len - 12, -1, -1):
                self._avg_vals[key].append(self.average(data[key][i:arr_len-k]))
                k += 1

            self._avg_vals[key].reverse()

        return {'hours': data, 'averages': self._avg_vals}

    """
    counts basic average from input values
    """

    def average(self, hour_values):
        sum = 0
        for i in hour_values:
            if i is not None:
                sum += i

        return round(sum / 12, 3)
