import os


class Wind:
    def __init__(self):
        self.gust = []
        self.veind = []
        self.gust_path = os.getcwd() + '/airMonitor/static/air/GUST'
        self.veind_path = os.getcwd() + '/airMonitor/static/air/VEIND'

    def load_data(self):
        self.gust = [file for file in os.listdir(self.gust_path)]
        self.veind = [file for file in os.listdir(self.veind_path)]

        return {'gust': self.gust, 'veind': self.veind}
