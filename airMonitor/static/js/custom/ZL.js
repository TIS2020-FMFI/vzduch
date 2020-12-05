class ZL{
    constructor(name, dict, fill, bg_color) {
        this.name = name;
        this.data = dict;
        this.fill = fill;
        this.bg_color = bg_color;
    }
    get(stationName, number){
        console.log(stationName);
        let d = this.data[stationName];
        console.log(d);
        let n = number;
        if(n > d.length){
            n = d.length
        }
        console.log(d.length);
        console.log(n);
        console.log(d.slice(d.length - n, d.length ));
        return {"label": this.name,
                "fill": this.fill,
                "backgroundColor": this.bg_color,
                "borderColor": this.bg_color,
                "data": d.slice(d.length - n, d.length )} ;
    }
    keys(stationName){
        let result = [];
        for(let date in this.data[stationName]){
            result.push(date);
        }
        return result;
    }





}