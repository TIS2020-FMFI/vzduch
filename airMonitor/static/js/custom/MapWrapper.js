class MapWrapper{
    constructor(s) {
        this.stations = [];
        for(let i = 0; i < s.length; i++){
            this.stations.push(new Station(s[i]["name"], s[i]["lat"], s[i]["lon"]));
        }
        this.oldZoom = 7.2;

        this.hour = 0;
        this.pollutant = null;

        this.map = L.map('map', {
                minZoom: 7.2,
                zoom: 7.2,
                maxZoom: 11,
                center: [48.60, 19.30],
            });
        // this.map.setMaxBounds([[49.70, 16.00],[47.60, 22.60]]);
        let cartodbAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>';

        let position = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
                attribution: cartodbAttribution
            }).addTo(this.map);

        this.changePollutant("pm10");
        this.drawAllStations();
    }
    changePollutant(name){
        if(this.pollutant === name){
            return;
        }
        this.pollutant = name;
        for(let i = 0; i < this.stations.length; i++){
            this.stations[i].changePollutant(this.pollutant, chart.getValue(this.stations[i].name, this.pollutant, this.hour));
        }
    }
    changeHour(hour){
        if(this.hour === hour){
            return;
        }
        this.hour = hour;
        for(let i = 0; i < this.stations.length; i++){
            this.stations[i].changePollutant(this.pollutant, chart.getValue(this.stations[i].name, this.pollutant, this.hour));
        }
    }

    clearAllStations(){
        for(let i = 0; i < this.stations.length; i++){
            this.map.removeLayer(this.stations[i].circle);
        }
    }

    drawAllStations(){
        for(let i = 0; i < this.stations.length; i++){
            this.stations[i].addTo(this.map);
        }
    }
    resetMapPosition(){
        this.map.panTo( [48.60, 19.30]);
        this.map.zoomOut(10);
    }
}