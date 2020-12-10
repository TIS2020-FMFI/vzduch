class ChartWrapper{
    constructor(data) {
        this.data = data;
        this.zl = [];
        for(let k in data["data"]["datasets"]){
            let d = data["data"]["datasets"][k];
            this.zl.push(new ZL(d["label"], d["data"], d["fill"], d["backgroundColor"]))
        }
        this.labels = this.data["data"]["labels"];
        this.stationName = "BRATISLAVA,JESENIOVA";
        this.days = 1;
        this.hours = 0;
        this.setHours();

    }
    getChart(){
        let ctx = document.getElementById('canvas').getContext('2d');
        let dataset = []
        for(let z in this.zl){
            dataset.push(this.zl[z].get(this.stationName, this.hours));
        }
        this.data["data"]["datasets"] = dataset;
        this.data["data"]["labels"] = this.labels.slice(this.labels.length - this.hours - 1,
            this.labels.length);

        return new Chart(ctx, this.data)
    }
    setStation(station){
         this.stationName = station;
    }
    setDays(days){
         this.days = days;
         this.setHours();
    }
    setHours(){
        console.log(this.labels);
        this.hours = this.days * 24;
    }
    drawChart(){
         window.myLine = this.getChart();
    }



}