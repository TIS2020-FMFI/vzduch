from django.conf import settings
import os
import datetime


class Wind:
    def __init__(self):
        self.air_path = settings.AIR_PATH
        self.forecast_days = 1


    def load_data(self):
        date_dirs = [file for file in os.listdir(self.air_path)]
        date_dirs.sort(reverse=True)
        date_dirs = date_dirs[:self.forecast_days]

        wind_data = {'DIR_DATES': [], 'SELECT_DATES': [], 'PICTURES': dict()}
        for date_directory in date_dirs:
            date_time_obj = datetime.datetime.strptime(date_directory[:-3], '%Y-%m-%d')
            dir_date = date_time_obj.date().__str__() + '_00'
            select_date = str(date_time_obj.day) + '.' + str(date_time_obj.month) + '.' + str(date_time_obj.year)

            wind_data['PATH'] = str(self.air_path)
            wind_data['DIR_DATES'].append(dir_date)
            wind_data['SELECT_DATES'].append(select_date)
            wind_data['PICTURES'][dir_date] = {'GUST': [], 'VEIND': []}

            for picture_type in ['GUST', 'VEIND']:
                picture_path = os.path.join(self.air_path, date_directory, picture_type)
                for picture in os.listdir(picture_path):
                    wind_data['PICTURES'][dir_date][picture_type].append(picture)

        return wind_data