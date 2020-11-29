import json

from django.conf import settings


class Chart:
    def __init__(self):
        self._chart = dict()
        self._datasets = []
        self.load_defaults("airMonitor/static/default_chart.json")
        self._labels = list()
        self._data_colors = ["red", "orange", "yellow", "green", "blue", "purple"]

    def load_defaults(self, path):
        with open(path, "r") as file:
            self._chart = json.load(file)

    def add_colors(self):
        for index in range(len(self._datasets)):
            self._datasets[index]["backgroundColor"] = settings.DATA_COLORS[self._data_colors[index]]
            self._datasets[index]["borderColor"] = settings.DATA_COLORS[self._data_colors[index]]

    def add_label(self, label):
        if label not in self._labels:
            self._labels.append(label)

    def dict(self):
        self.add_colors()
        self._chart["data"] = {
            "labels": [str(x) for x in self._labels],
            "datasets": self._datasets
        }
        return self._chart

    def add_data(self, station, zl, data):
        for dataset in self._datasets:
            if dataset["label"] == zl:
                if station not in dataset["data"]:
                    dataset["data"][station] = []
                dataset["data"][station].append(data)
                return
        self._datasets.append({
            "label": zl,
            "data": {station: [data, ]},
            "fill": False
        })
