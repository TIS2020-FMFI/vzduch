import json


class Chart:
    def __init__(self):
        with open("airMonitor/static/default_chart.json", "r") as file:
            self._chart = json.load(file)
        self._data = dict()

    def export_data(self):
        result = []
        for key in self._data:
            result.append({"name": key, "data": self._data[key]})

        return result

    def dict(self):
        self._chart["series"] = self.export_data()
        return self._chart

    def add_data(self, key, value):
        if key not in self._data:
            self._data[key] = []
        self._data[key].append(value)
