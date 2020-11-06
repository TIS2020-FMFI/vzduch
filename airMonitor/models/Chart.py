import json


class Chart:
    def __init__(self):
        self._chart = dict()
        self._data = dict()
        self.load_defaults("airMonitor/static/default_chart.json")

    def load_defaults(self, path):
        with open(path, "r") as file:
            self._chart = json.load(file)

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
