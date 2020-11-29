class Station{
    constructor(name, lat, lon, color, color_code, zl) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.color = color;
        this.color_code = color_code;
        this.zl = zl;
        this.radius = 2000;
        this.circle = L.circle(this.getLocation(),{
                color: this.color,
                fillColor: this.color_code,
                fillOpacity: 0.1,
                radius: this.radius
            });
    }
    getLocation(){
        return [this.lat, this.lon];
    }

    getCircle(){
        this.circle = L.circle(this.getLocation(),{
                color: this.color,
                fillColor: this.color_code,
                fillOpacity: 1,
                radius: this.radius
            });
        this.circle.bindPopup(this.name + ': ' + this.zl);
        this.circle.on('mouseover', function (e){
            this.openPopup();
        });
        this.circle.on('mouseout', function (e){
            this.closePopup();
        });
        return this.circle;
    }
    addTo(map){
        this.getCircle().addTo(map);
    }

    increaseSize(){
        this.radius *= 2;
    }

    decreaseSize(){
        this.radius /= 2;
    }
}