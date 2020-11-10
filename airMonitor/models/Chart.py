import json

data_colors = {
    "red": "rgb(255, 99, 132)",
    "orange": "rgb(255, 159, 64)",
    "yellow": "rgb(255, 205, 86)",
    "green": "rgb(75, 192, 192)",
    "blue": "rgb(54, 162, 235)",
    "purple": "rgb(153, 102, 255)",
    "grey": "rgb(201, 203, 207)"
}


class Chart:
    def __init__(self):
        self._chart = dict()
        self._datasets = []
        self.load_defaults("airMonitor/static/default_chart.json")
        self._labels = list()
        self._data_colors = ["red", "orange", "yellow", "green", "blue", "purple", "grey"]

    def load_defaults(self, path):
        with open(path, "r") as file:
            self._chart = json.load(file)

    def add_colors(self):
        for index in range(len(self._datasets)):
            self._datasets[index]["backgroundColor"] = data_colors[self._data_colors[index]]
            self._datasets[index]["borderColor"] = data_colors[self._data_colors[index]]

    def add_label(self, label):
        if label not in self._labels:
            self._labels.append(label)

    def dict(self):
        self.add_colors()
        self._chart["data"] = {
           "labels": self._labels,
            "datasets": self._datasets
        }
        return self._chart

    def add_data(self, label, data):
        for dataset in self._datasets:
            if dataset["label"] == label:
                dataset["data"].append(data)
                return
        self._datasets.append({
            "label": label,
            "data": [data, ],
            "fill": False
        })
