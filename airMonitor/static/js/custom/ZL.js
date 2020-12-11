class ZL{
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
        this.added_values = {}
        for(let station in dict){
            this.added_values[station] = [];
        }
    }

    get(stationName, number){
        let d = this.data[stationName];
        let n = number;
        if(n > d.length){
            n = d.length
        }
        for(let value in this.added_values[stationName]){
            d.push(value);
        }
        return {"label": this.name,
                "fill": this.fill,
                "backgroundColor": this.bg_color,
                "borderColor": this.bg_color,
                "data": d.slice(d.length - n, d.length )} ;
    }

    addValue(stationName, hour, value){
        /*console.log("                                      ");
        console.log(this.added_values[stationName].length === hour);
        console.log(this.added_values[stationName]);
        console.log(hour);
        console.log("                                      ");*/
        if(this.added_values[stationName].length === hour){
            this.added_values[stationName][hour - 1] = value;
            return false;
        }
        console.log("pushujem");
        this.added_values[stationName].push(value);
        return true;
    }

    pop(stationName){
        this.added_values[stationName].pop()
    }

}