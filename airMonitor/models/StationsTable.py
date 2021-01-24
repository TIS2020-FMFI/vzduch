import json
import datetime
import math


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

    def _get_stations(self, data):
        """Internal function, gets all stations from data

        Parameters
        ----------
        data : Chart
            Measured values

        Returns
        -------
        dict[str, dict]
            Dictionary with structure - station: empty dictionary
        """

        stations = list(data.get_values('pm10')['data'].keys())
        return {station: {} for station in stations}

    def _get_hour_values(self, data):
        """Internal function, gets hour values from data for stations table

        Parameters
        ----------
        data : Chart
            Measured values

        Returns
        -------
        list[dict[str, Any]]
            Hour values for stations table
        """

        hour_values = self._get_stations(data)
        for material in self._POLLUTING_MATERIALS:
            values = data.get_values(material)['data']
            for station in hour_values.keys():
                hour_values[station][material] = list(reversed(values[station][-self._HOUR_RANGE:]))
        return hour_values

    def _get_outages(self, values):
        """Internal function, gets outages for stations table

        Parameters
        ----------
        values : dict[str, dict[str, Any]]
            Measured values

        Returns
        -------
        list[dict[str, Any]]
            Outages
        """

        outages = []
        for value_dict in values:
            station = value_dict.pop('name')
            outages.append({k: list(map(lambda x: None if math.isnan(x) else x, v)).count(None) for k, v in value_dict.items()})
            outages[-1]['name'] = station
            value_dict['name'] = station

        return outages

    def _adjust_values(self, values):
        """Internal function, adjusts values to required form for stations table

        Parameters
        ----------
        values : dict[str, dict[str, Any]]
            Values of which form need to be changed

        Returns
        -------
        list[dict[str, Any]]
            Adjusted values
        """

        adjusted_values = []
        for station in values.keys():
            adjusted_values.append(values[station])  # mutable!
            adjusted_values[-1]['name'] = self._get_station_name(station)
        return sorted(adjusted_values, key=lambda x: x['name'])

    def _process_data(self, data, date):
        """Internal function, processes data for stations table

        Parameters
        ----------
        data : Chart
            Measured values
        date : datetime
            Date from which data are taken

        Returns
        -------
        dict[str, Any]
            Processed data
        """

        values_dict = {}
        values_dict['hour'] = self._adjust_values(self._get_hour_values(data))
        values_dict['max'] = self._adjust_values(data.get_maximal_values(str(date.day)))
        values_dict['nulls'] = self._get_outages(values_dict['hour'])
        return values_dict

    def prepare_data(self, data, date):
        """Adjusts data to their required form for stations table

        Parameters
        ----------
        data : Chart
            Measured values
        date : datetime
            Date from which data are taken

        Returns
        -------
        dict[str, Any]
            Data for stations table
        """

        table_data = self._process_data(data, date)
        table_header = ['name'] + list(self._POLLUTING_MATERIALS)
        return {'thead': json.dumps(table_header), 'tbody': json.dumps(table_data).replace("NaN", "null")}
