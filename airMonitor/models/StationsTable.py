import json
import datetime

from airMonitor.models.SHMU import ObsNmsko1H, Si
from airMonitor.models.Station import Station


def _get_column(column, list_of_tuples):
    return list(map(lambda x: x[column], list_of_tuples))


def _max(list_):
    list_ = [val for val in list_ if val is not None]
    return max(list_) if len(list_) > 0 else None


class StationsTable:
    def __init__(self):
        # order of polluting materials influences their order in table on page
        self._POLLUTING_MATERIALS = ('pm10', 'so2', 'o3', 'no2', 'pm2_5')
        self._HOUR_RANGE = 24
        self._PARAMETER_OPTIONS = ('hour', 'max', 'nulls')
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
            'KOLONICKESEDLO': 'Kolonické sedlo',
            'NMSKOID99126': 'NMSKOID99126',
            'NMSKOID99130': 'NMSKOID99130',
            'NMSKOID99223': 'NMSKOID99223',
            'NMSKOID99350': 'NMSKOID99350',
            'NMSKOID99501': 'NMSKOID99501',
            'NMSKOID99502': 'NMSKOID99502',
            'NMSKOID99503': 'NMSKOID99503',
            'NMSKOID99701': 'NMSKOID99701',
            'NMSKOID99702': 'NMSKOID99702',
            'NMSKOID99703': 'NMSKOID99703',
            'NMSKOID99801': 'NMSKOID99801',
            'NMSKOID99802': 'NMSKOID99802',
            'NMSKOID99808': 'NMSKOID99808'
        }

    def _convert_to_dict(self, values):  # values = [(id, *polluting_materials)]
        ids = set(map(lambda x: x[0], values))
        values_dict = {id_: [] for id_ in ids}
        for val in values:
            values_dict[val[0]].append(val[1:])
        n = len(self._POLLUTING_MATERIALS)
        for id_ in values_dict.keys():
            values_dict[id_] = {self._POLLUTING_MATERIALS[i]: _get_column(i, values_dict[id_]) for i in range(n)}
            for material in values_dict[id_].keys():
                measured_values = values_dict[id_][material]
                values_dict[id_][material] = [
                    measured_values[0],
                    _max(measured_values),
                    self._HOUR_RANGE - len(measured_values) + measured_values.count(None)
                ]
        return values_dict

    def _join_stations_and_values(self, stations, values):
        stations_with_values = stations
        for id_ in stations.keys():
            for material in self._POLLUTING_MATERIALS:
                if id_ in values:
                    stations_with_values[id_][material] = values[id_][material]  # reference to mutable!!!
                else:
                    stations_with_values[id_][material] = [None, None, self._HOUR_RANGE]
        return stations_with_values

    def _create_table_data(self, stations_values):
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

    def load_data(self):
        stations_raw = [(x.get_station().id, x.get_station().name) for x in Station.all()]
        stations = {id_: {'name': self._REAL_STATION_NAMES[name]} for id_, name in stations_raw}
        time_range = (datetime.datetime(2020, 3, 30, 1), datetime.datetime(2020, 3, 31, 0))
        # time_range = (datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(hours=self._HOUR_RANGE))
        measured_values_raw = list(ObsNmsko1H.objects.filter(date__range=time_range).order_by('-date')
                                   .values_list('si', *self._POLLUTING_MATERIALS))
        measured_values = self._convert_to_dict(measured_values_raw)  # {id: {material: [hour, max, nulls]}}
        stations_with_values = self._join_stations_and_values(stations, measured_values)
        data = self._create_table_data(list(stations_with_values.values()))
        table_header = ['name'] + list(self._POLLUTING_MATERIALS)
        return {'thead': json.dumps(table_header), 'tbody': json.dumps(data)}
