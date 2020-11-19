class Station{
    constructor(name, lat, lon, color, color_code, zl) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.color = color;
        this.color_code = color_code;
        this.zl = zl;
        this.circle = L.circle(this.getLocation(),{
                color: this.color,
                fillColor: this.color_code,
                fillOpacity: 0.5,
                radius: 1000
            });
    }
    getLocation(){
        return [this.lat, this.lon];
    }

    getCircle(){
        return this.circle;
    }
    addTo(map){
        this.circle.addTo(map);
    }
}