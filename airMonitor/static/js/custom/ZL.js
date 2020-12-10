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
    }

    get(stationName, number){
        let d = this.data[stationName];
        let n = number;
        if(n > d.length){
            n = d.length
        }
        return {"label": this.name,
                "fill": this.fill,
                "backgroundColor": this.bg_color,
                "borderColor": this.bg_color,
                "data": d.slice(d.length - n, d.length )} ;
    }

    addValue(stationName, value){
        this.data[stationName].push(value);
    }

    pop(stationName){
        return this.data[stationName].pop();
    }

}