class Station{
    constructor(name, lat, lon, color, color_code, zl) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.color = color;
        this.color_code = color_code;
        this.zl = zl;
        this.radius = 5;
        this.circle = L.circleMarker(this.getLocation(),{
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
        this.circle = L.circleMarker(this.getLocation(),{
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
        this.circle.on('click', function (e){
            let findName = this.getPopup().getContent().split(":");
            let stationName = findName[0];
            chart.setStation(stationName);
            chart.drawChart();
            avgTable.updateTable(stationName);
            let sel = document.getElementById('id_stations');
            for(let i = 0; i < sel.options.length;i++){
                if(sel.options[i].text === stationName){
                    sel.options[i].selected = true;
                }
            }

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