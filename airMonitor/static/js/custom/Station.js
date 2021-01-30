class Station{
    constructor(name, lat, lon) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.color = null;
        this.color_code = null;
        this.pollutant = null;
        this.value = null;
        this.radius = 5;
        this.circle = null
        this.color_dict = {
            0: ["grey", "#efefef"],
            1: ["green", "#00b050"],
            2: ["light green", "#92d050"],
            3: ["yellow", "#ffff00"],
            4: ["orange", "#ffc000"],
            5: ["red", "#ff0000"]
        }
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
        this.circle.bindPopup(this.name + ': ' + this.pollutant + "( " + this.value + " )");
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
    changeColor(color){
        this.color = color[0];
        this.color_code = color[1];
    }
    changePollutant(pollutant, value){
        this.pollutant = pollutant;
        this.value = value;
        let level = chart.getPollutantLevel(pollutant, value);
        this.changeColor(this.color_dict[level]);
    }
}