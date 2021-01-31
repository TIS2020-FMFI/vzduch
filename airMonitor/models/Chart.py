import json

from django.conf import settings


class Chart:
    def __init__(self):
        self._chart = dict()
        self._data = dict()
        self._avg_12 = dict()
        self._avg_24 = dict()
        self._datasets = list()
        self._labels = list()
        self._stations = set()
        self._pollutant = settings.POLLUTANTS
        self._data_colors = list(settings.DATA_COLORS.keys())

        self.load_defaults("airMonitor/static/default_chart.json")

    def load_defaults(self, path):
        with open(path, "r") as file:
            self._chart = json.load(file)
        self._chart["limits"] = settings.POLLUTANTS_LIMIT

    def add_colors(self):
        k = 0
        for index in range(len(self._datasets)):
            pollutant = self._datasets[index]["label"]
            if pollutant in settings.POLLUTANTS:
                color_index = settings.POLLUTANTS.index(pollutant)
            else:
                color_index = len(settings.POLLUTANTS) + k
                k += 1
            self._datasets[index]["backgroundColor"] = settings.DATA_COLORS[self._data_colors[color_index]]
            self._datasets[index]["borderColor"] = settings.DATA_COLORS[self._data_colors[color_index]]

    def add_label(self, label):
        if label not in self._labels:
            self._labels.append(label)

    def normalize_data(self):
        self._generate_datasets()
        self._generate_labels()

    def dict(self):
        self._chart["data"] = {
            "labels": [str(x) for x in self._labels],
            "datasets": self._datasets
        }
        return self._chart

    def add_data(self, date,  station, pollutant, data):
        if pollutant == "12-hour":
            if station not in self._avg_12:
                self._avg_12[station] = []
            self._avg_12[station].append(data)
            return
        if pollutant == "24-hour":
            if station not in self._avg_24:
                self._avg_24[station] = []
            self._avg_24[station].append(data)
            return
        self._stations.add(station)
        if date not in self._data:
            self._data[date] = dict()
        if pollutant not in self._data[date]:
            self._data[date][pollutant] = dict()
        self._data[date][pollutant][station] = data

    def get_values(self, pollutant):
        if len(self._datasets) == 0:
            self._generate_datasets()
        for data in self._datasets:
            if data["label"] == pollutant:
                return data

    def get_outages(self, day):
        outage_data = dict()
        for date in self._data:
            if date.split(".")[0] != day:
                continue

            for station in self._stations:
                if station not in outage_data:
                    outage_data[station] = dict()
                for pollutant in self._pollutant:
                    if pollutant not in outage_data[station]:
                        outage_data[station][pollutant] = 0
                    if station not in self._data[date][pollutant]:
                        outage_data[station][pollutant] += 1
                    elif self._data[date][pollutant][station] is None:
                        outage_data[station][pollutant] += 1
        return outage_data

    def get_maximal_values(self, day):
        maximal_values = dict()
        for date in self._data:
            if date.split(".")[0] != day:
                continue

            for station in self._stations:
                if station not in maximal_values:
                    maximal_values[station] = dict()
                for pollutant in self._pollutant:
                    if pollutant not in maximal_values[station]:
                        maximal_values[station][pollutant] = 0
                    if station in self._data[date][pollutant]:
                        if self._data[date][pollutant][station] is None:
                            continue
                        maximal_values[station][pollutant] = max(self._data[date][pollutant][station],
                                                                 maximal_values[station][pollutant])
        return maximal_values

    def _generate_datasets(self):
        self._datasets = []
        for pollutant in self._pollutant:
            self._datasets.append({
                "label": pollutant,
                "data": dict(),
                "fill": False
            })
        pollutant_data = dict()
        for date in self._data:
            for pollutant in self._pollutant:
                if pollutant not in pollutant_data:
                    pollutant_data[pollutant] = dict()
                for station in self._stations:
                    if station not in pollutant_data[pollutant]:
                        pollutant_data[pollutant][station] = []
                    if station in self._data[date][pollutant]:
                        pollutant_data[pollutant][station].append(self._data[date][pollutant][station])
                    else:
                        pollutant_data[pollutant][station].append(None)

        for i in range(len(self._datasets)):
            self._datasets[i]["data"] = pollutant_data[self._datasets[i]["label"]]

        self._datasets.append({
            "label": "12-hour",
            "data": self._avg_12,
            "fill": False
        })
        try:
            self._datasets.append({
                "label": "24-hour",
                "data": self._filter_dataset(self._avg_24),
                "fill": False,
                "pointRadius": 10
            })
        except:
            self._datasets.append({
                "label": "24-hour",
                "data": self._avg_24,
                "fill": False,
                "pointRadius": 10
            })


    def _filter_dataset(self, dataset):
        result = dict()
        self._generate_labels()
        for i in range(len(self._labels)):
            for station in dataset:
                if station not in result:
                    result[station] = []
                if "00:00" in self._labels[i]:
                    result[station].append(dataset[station][i])
                else:
                    result[station].append(None)
        return result

    def _generate_labels(self):
        self._labels = []
        for date in self._data:
            if date is None:
                continue
            self._labels.append(date)
