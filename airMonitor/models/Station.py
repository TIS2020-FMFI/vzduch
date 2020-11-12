from airMonitor.models.SHMU import Si


class Station(Si):
    color_name = None
    color_code = None

    class Meta:
        managed = False
        db_table = 'si'

    def set_color(self, color_name, color_code):
        self.color_name = color_name
        self.color_code = color_code

