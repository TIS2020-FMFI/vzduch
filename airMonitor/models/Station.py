from airMonitor.models.SHMU import Si


class Station(Si):
    color = None
    
    class Meta:
        managed = False
        db_table = 'si'

    def set_color(self, color_name, color_code):
        self.color_name = color_name
        self.color_code = color_code

    def get(self):
        position = [self.lat, self.lon]
        args = {
            "color": self.color,
            "fillColor": self.color,
            "fillOpacity": 0.5,
            "radius": 5000,
        }
        return {"position": position, "options": args}
