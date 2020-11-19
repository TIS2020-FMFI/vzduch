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