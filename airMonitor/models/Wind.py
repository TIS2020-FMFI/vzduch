from django.conf import settings
import os
import datetime
import re

class Wind:
    def __init__(self):
        self.air_path = settings.AIR_PATH
        self.forecast_dirs = 7
        self.HOUR_IN_SECONDS = 3600

    def load_data(self):
        all_dirs = [file for file in os.listdir(self.air_path)]
        all_dirs.sort(reverse=True)
        date_dirs = []
        for directory in all_dirs:
            if re.match('\d{4}-\d{2}-\d{2}_\d{2}', directory):
                date_dirs.append(directory)
            if len(date_dirs) == self.forecast_dirs:
                date_dirs.reverse()
                break

        wind_data = {'DIR_DATES': [], 'SELECT_DATES': [], 'PICTURES': dict(), 'PATH': str(self.air_path)}

        current_datetime = datetime.datetime.now()

        for i, date_directory in enumerate(date_dirs):
            date_time_obj = datetime.datetime.strptime(date_directory, '%Y-%m-%d_%H')
            select_date = str(date_time_obj.day) + '.' + str(date_time_obj.month) + '.' + str(date_time_obj.year) + ' ' + str(date_time_obj.hour) + ':00'

            default_picture_index = (current_datetime - date_time_obj).total_seconds() // self.HOUR_IN_SECONDS
            wind_data['INDEX'] = default_picture_index

            wind_data['DIR_DATES'].append(date_directory)
            wind_data['SELECT_DATES'].append(select_date)
            wind_data['PICTURES'][date_directory] = {'GUST': [], 'VEIND': []}

            for picture_type in ['GUST', 'VEIND']:
                picture_path = os.path.join(self.air_path, date_directory, picture_type)
                for picture in os.listdir(picture_path):
                    wind_data['PICTURES'][date_directory][picture_type].append(picture)

        return wind_data
