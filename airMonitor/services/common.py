from django.conf import settings


def add_colors(stations, zl):
    for i in range(len(stations)):
        mx = 0
        rows = filter_list_stations(zl, stations[i].get_station().id)
        max_pollutants = dict()
        for row in rows:
            for pollutant in settings.POLLUTANTS:
                if pollutant not in max_pollutants:
                    max_pollutants[pollutant] = -1
                value = max_pollutants[pollutant]
                max_pollutants[pollutant] = max(value, row.__dict__[pollutant])

        for pollutant in settings.POLLUTANTS:
            for j in range(1, 5):
                if pollutant not in max_pollutants:
                    max_pollutants[pollutant] = 0
                    break
                if max_pollutants[pollutant] == -1:
                    max_pollutants[pollutant] = 0
                    break
                if max_pollutants[pollutant] < settings.POLLUTANTS_LIMIT[pollutant][j]:
                    max_pollutants[pollutant] = j
                    break
                if j == 4:
                    max_pollutants[pollutant] = 5
        mx = settings.POLLUTANTS[0]
        for pollutant in settings.POLLUTANTS:
            if max_pollutants[pollutant] > max_pollutants[mx]:
                mx = pollutant
        stations[i].set_zl(mx)
        mx = max_pollutants[mx]
        stations[i].set_color(settings.COLORS[mx][0], settings.COLORS[mx][1])
    return stations


def filter_list_stations(inp, station):
    result = []
    for r in inp:
        if r.si.id == station:
            result.append(r)
    return result


