import json
import datetime

from airMonitor.models.SHMU import ObsNmsko1H
from airMonitor.models.Station import Station


def _get_column(column, list_of_tuples):
    """Internal function for getting column from 2D array"""
    return list(map(lambda x: x[column], list_of_tuples))


def _max_with_nulls(list_):
    """Internal function for finding max value in list, which can contain None values"""
    list_ = [val for val in list_ if val is not None]
    return max(list_) if len(list_) > 0 else None


class StationsTable:
    """
    Class used for loading data for table of stations on page

    Methods
    -------
    load_data() : dict
        Loads data from database
    """

    def __init__(self):
        # order of polluting materials influences their order in table on page
        self._POLLUTING_MATERIALS = ('pm10', 'so2', 'o3', 'no2', 'pm2_5')
        self._HOUR_RANGE = 25
        self._PARAMETER_OPTIONS = ('hour', 'max', 'nulls')
        self.date = None
        self._REAL_STATION_NAMES = {
            'BRATISLAVA,JESENIOVA': 'Bratislava, Jeséniova',
            'CHOPOK,EMEP': 'Chopok, EMEP',
            'GANOVCE,METEO.ST.': 'Gánovce, Meteo. st.',
            'KOJSOVSKAHOLA': 'Kojšovská Hoľa',
            'BRATISLAVA,MAMATEYOVA': 'Bratislava, Mamateyova',
            'BRATISLAVA,TRNAVSKEMYTO': 'Bratislava, Trnavské Mýto',
            'BRATISLAVA,KAMENNENAM.': 'Bratislava, Kamenné nám.',
            'SENICA,HVIEZDOSLAVOVA': 'Senica, Hviezdoslavova',
            'TRNAVA,KOLLAROVA': 'Trnava, Kollárova',
            'TRENCIN,HASICSKA': 'Trenčín, Hasičská',
            'MALACKY,MIEROVENAMESTIE': 'Malacky, Mierové námestie',
            'NITRA,JANIKOVCE': 'Nitra, Janíkovce',
            'NITRA,STUROVA': 'Nitra, Štúrova',
            'BANSKABYSTRICA,STEFANIKOVONABREZIE': 'Banská Bystrica, Štefánikovo nábrežie',
            'BANSKABYSTRICA,ZELENA': 'Banská Bystrica, Zelená',
            'RUZOMBEROK,RIADOK': 'Ružomberok, Riadok',
            'ZIARNADHRONOM,JILEMNICKEHO': 'Žiar nad Hronom, Jilemnického',
            'BYSTRICANY,ROZVODNASSE': 'Bystričany, Rozvodňa SSE',
            'HANDLOVA,MOROVIANSKACESTA': 'Handlová, Morovianska cesta',
            'PRIEVIDZA,MALONECPALSKA': 'Prievidza, Malonecpalská',
            'ZILINA,OBEZNA': 'Žilina, Obežná',
            'HNUSTA,HLAVNA': 'Hnúšta, Hlavná',
            'ZVOLEN,J.ALEXYHO': 'Zvolen, J. Alexyho',
            'MARTIN,JESENSKEHO': 'Martin, Jesenského',
            'JELSAVA,JESENSKEHO': 'Jelšava, Jesenského',
            'KOSICE,STEFANIKOVA': 'Košice, Štefánikova',
            'KOSICE,DUMBIERSKA': 'Košice, Ďumbierska',
            'VELKAIDA,LETNA': 'Veľká Ida, Letná',
            'KOSICE,AMURSKA': 'Košice, Amurská',
            'PRESOV,ARM.GEN.L.SVOBODU': 'Prešov, Arm.gen. Ľ. Svobodu',
            'KROMPACHY,SNP': 'Krompachy, SNP',
            'HUMENNE,NAM.SLOBODY': 'Humenné, Nám. slobody',
            'STRAZSKE,MIEROVA': 'Strážske, Mierová',
            'VRANOVNADTOPLOU,M.R.STEFANIKA': 'Vranov nad Top., M.R.Štefánika',
            'TOPOLNIKY,ASZOD,EMEP': 'Topoľníky, Aszód, EMEP',
            'STARINA,VODNANADRZ,EMEP': 'Starina, Vodná nádrž, EMEP',
            'STARALESNA,AUSAV,EMEP': 'Stará Lesná, AÚ SAV, EMEP',
            'KOLONICKESEDLO': 'Kolonické sedlo'
        }

    def _get_station_name(self, name):
        """Internal function, gets real station name if known

        Parameters
        ----------
        name : str
            Station name

        Returns
        -------
        str
            Real station name if known else name given
        """

        return self._REAL_STATION_NAMES[name] if name in self._REAL_STATION_NAMES else name

    def _get_stations(self):
        """Internal function, gets station ids with responsive names from database

        Returns
        -------
        dict[int, dict[str, str]]
            Station ids with names
        """

        stations_raw = [(s.get_station().id, s.get_station().name) for s in Station.all()]
        return {id_: {'name': self._get_station_name(name)} for id_, name in stations_raw}

    def _convert_raw_values_to_dict(self, values):  # values = [(id, *polluting_materials)]
        """Internal function, converts values from database to dictionary

        Parameters
        ----------
        values : list[(int, ...)]
            Measured values from database

        Returns
        -------
        dict
            Measured values as dictionary
        """

        ids = set(map(lambda x: x[0], values))
        values_dict = {id_: [] for id_ in ids}
        for val in values:
            values_dict[val[0]].append(val[1:])
        n = len(self._POLLUTING_MATERIALS)
        for id_ in values_dict.keys():
            values_dict[id_] = {self._POLLUTING_MATERIALS[i]: _get_column(i, values_dict[id_]) for i in range(n)}
            for material in values_dict[id_].keys():
                measured_values = [None if x is None else round(x, 1) for x in values_dict[id_][material]]
                values_dict[id_][material] = [
                    measured_values[:] + [None] * (self._HOUR_RANGE - len(measured_values)),
                    _max_with_nulls(measured_values),
                    self._HOUR_RANGE - len(measured_values) + measured_values.count(None)
                ]
        return values_dict  # {id: {material: [[hour], max, nulls]}}

    def _get_measured_values(self):
        """Internal function, gets station id with responsive measured values from given period of time

        Returns
        -------
        dict
            Measured values
        """

        # time_range = (datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(hours=self._HOUR_RANGE))
        time_range = (self.date, self.date + datetime.timedelta(hours=self._HOUR_RANGE)) # test
        measured_values_raw = list(ObsNmsko1H.objects.filter(date__range=time_range).order_by('-date')
                                   .values_list('si', *self._POLLUTING_MATERIALS))
        return self._convert_raw_values_to_dict(measured_values_raw)

    def _join_stations_and_values(self, stations, values):
        """Internal function, joins stations and measured values from database based on station id

        Parameters
        ----------
        stations : dict[int, dict[str, str]]
            Station names with ids
        values : dict
            Measured values with station ids

        Returns
        -------
        list[dict]
            List of station names with measured values
        """

        stations_with_values = stations
        for id_ in stations.keys():
            for material in self._POLLUTING_MATERIALS:
                if id_ in values:
                    stations_with_values[id_][material] = values[id_][material]  # reference to mutable!!!
                else:
                    stations_with_values[id_][material] = [None, None, self._HOUR_RANGE]
        return list(stations_with_values.values())

    def _get_stations_with_values(self):
        """Internal function, gets station names with responsive measured values

        Returns
        -------
        list[dict]
            List of station names with measured values
        """

        stations = self._get_stations()
        measured_values = self._get_measured_values()
        return self._join_stations_and_values(stations, measured_values)

    def _create_table_data(self, stations_values):
        """Internal function, creates data for stations table

        Parameters
        ----------
        stations_values : list[dict]
            List of station names with measured values

        Returns
        -------
        dict[str, Any]
            Data for stations table
        """

        values_dict = {}
        for i in range(len(self._PARAMETER_OPTIONS)):
            option = self._PARAMETER_OPTIONS[i]
            values_dict[option] = []
            for data in stations_values:
                station_name = data.pop('name')
                values_dict[option].append({material: value[i] for material, value in data.items()})
                values_dict[option][-1]['name'] = station_name
                data['name'] = station_name
        return values_dict

    def load_data(self, date):
        """Loads data from database from given period of time

                Returns
                -------
                dict[str, Any]
                    Table data and table headers for stations table
                """

        self.date = date
        table_data = self._create_table_data(self._get_stations_with_values())
        table_header = ['name'] + list(self._POLLUTING_MATERIALS)
        return {'thead': json.dumps(table_header), 'tbody': json.dumps(table_data)}
