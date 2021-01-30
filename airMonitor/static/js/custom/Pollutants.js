class Pollutants{
    /***
     * @param name - name of the zl
     * @param dict - data in form of dict that contains station name as key
     *               and array of values for last 7 days as value
     * @param fill - name of color that the zl should be displayed with
     * @param bg_color - hex code of the color
     */
    constructor(name, dict, fill, bg_color) {
        this.name = name;
        this.data = dict;
        this.fill = fill;
        this.bg_color = bg_color;
        this.added_values = {};
        for(let station in dict){
            this.added_values[station] = [];
            for(let i = 0; i < 5; i++){
                this.added_values[station].push(null);
            }
        }
        for(let station in this.data){
            for(let i = 0; i < this.data[station].length; i++){
                let parsed_value = parseFloat(this.data[station][i]);
                if(isNaN(parsed_value)){
                    continue;
                }
                this.data[station][i] = parsed_value.toFixed(1).toString();
            }
        }
    }

    get(stationName, number){
        let d = this.data[stationName];
        if(undefined === d){
            d = [];
        }
        let n = number + 1;
        if(n > d.length){
            n = d.length
        }
        return {"label": this.name,
                "fill": this.fill,
                "backgroundColor": this.bg_color,
                "borderColor": this.bg_color,
                "data": d.slice(d.length - n, d.length ).concat(this.added_values[stationName])} ;
    }

    getValue(station, hour){
        let d = this.data[station];
        if(d === null || d === undefined){
            return null;
        }
        return d[d.length - 1 - hour];
    }

    addValue(stationName, hour, value){
        this.added_values[stationName][hour] = value
    }

    remove(stationName, hour){
        this.added_values[stationName][hour] = null;
    }

}