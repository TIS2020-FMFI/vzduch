from django.conf import settings


def add_colors(stations, zl):
    for i in range(len(stations)):
        mx = 0
        z = zl.filter(si=stations[i].get_station()).first()
        if z is not None:
            pom = [[x, z.__dict__[x]] for x in settings.ZL_LIMIT]
            for k in range(len(pom)):
                for j in range(1, 5):
                    if pom[k][1] is None:
                        pom[k][1] = 0
                        break
                    if pom[k][1] < settings.ZL_LIMIT[pom[k][0]][j]:
                        pom[k][1] = j
                        break
                    if j == 4:
                        pom[k][1] = 5
            print(stations[i], pom)
            mx = pom[0]
            for k in pom:
                if k[1] > mx[1]:
                    mx = k
            stations[i].set_zl(mx[0])
            mx = mx[1]

        print(i)
        print(mx)

        stations[i].set_color(settings.COLORS[mx][0], settings.COLORS[mx][1])
    return stations
