// import Leaflet from "leaflet/leaflet.js";

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

class MapWrapper{
    constructor(s) {
        this.stations = [];
        for(let i = 0; i < s.length; i++){
            this.stations.push(new Station(s[i]["name"], s[i]["lat"], s[i]["lon"],
                s[i]["color_name"], s[i]["color_code"], s[i]["zl"]));
        }
        this.map = L.map('map', {
                minZoom: 7.2,
                zoom: 7.2,
                maxZoom: 9,
                center: [48.60, 19.30],
            });
        this.map.setMaxBounds([[49.70, 16.00],[47.60, 22.60]])

        let cartodbAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>';

        let position = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
                attribution: cartodbAttribution
            }).addTo(this.map);
    }
    drawAllStations(){
        for(let i = 0; i < this.stations.length; i++){
            this.stations[i].addTo(this.map);
        }
    }





}