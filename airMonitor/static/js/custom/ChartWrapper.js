class ChartWrapper{
    constructor(data) {
        this.data = data;

        // Set limits for all zl
        this.limits = data["limits"]
        data["limits"] = null;

        // Create all Zl and push them into zl array
        this.zl = [];
        for (let k in data["data"]["datasets"]) {
            let d = data["data"]["datasets"][k];
            this.zl.push(new ZL(d["label"], d["data"], d["fill"], d["backgroundColor"]))
        }

        // All labels
        this.labels = this.data["data"]["labels"];

        // Default values for chart
        this.stationName = "BRATISLAVA,JESENIOVA";
        this.days = 1;
        this.hours = 0;
        this.setHours();

        // booleans for chart design
        this.show_line = true;
        this.tension = false;

        // Custom handler
        this.data["options"]["legend"]["onClick"] = this.legendHandler;

        // ChartJs item
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.chart = new Chart(this.ctx, this.data);
    }

    getChart(){
        this.updateChart();
        return this.chart;
    }
    setStation(station){
         this.stationName = station;
    }
    setDays(days){
         this.days = days;
         this.setHours();
    }
    setHours(){
        this.hours = this.days * 24;
    }
    drawChart(){
        this.getChart();
        window.myLine = this.chart;
    }

    /***
     *  Function that collect all data and updated chart according to them
     */
    updateChart(){
        let dataset = []
        for(let z in this.zl){
            let data;
            data = this.zl[z].get(this.stationName, this.hours)
            if(!this.show_line) {
                data["showLine"] = this.show_line;
            }
            dataset.push(data);
        }
        this.data["data"]["datasets"] = dataset;
        if(this.hours - 6 > this.labels.length){
            this.data["data"]["labels"] = this.labels;
        }
        else {
            this.data["data"]["labels"] = this.labels.slice(this.labels.length - this.hours - 6,
                this.labels.length);
        }

        if(this.tension){
            this.data["options"]["elements"]["line"]["tension"] = 0.5;
        }
        else{
            this.data["options"]["elements"]["line"]["tension"] = 0;
        }
        this.chart.update({
            "lazy": true,
            "duration": 0,
        })
    }

    /***
     * @param show - boolean that says whether to show lines or not
     */

    showLine(show){
        this.show_line = show;
    }

    /***
     * @param show - boolean that says whether to show tension or not
     */

    showTension(show){
        this.show_line = true;
        this.tension = show;
    }

    /***
     * Custom handler for legend in chart
     *
     * @param e - event
     * @param legendItem - item that is clicked on
     */
    legendHandler(e, legendItem) {
        let index = legendItem.datasetIndex;
        let ci = this.chart;
        let meta = ci.getDatasetMeta(index);

        meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;

        if(this.chart.getVisibleDatasetCount() <= 3){
            chart.processLabels()
        }

        ci.update({
            "duration": 0,
            "lazy": true,
        });
    }

    /***
     *
     *  Function for processing which zl are selected and draw lines depending on their limits
     *
     */

    processLabels(){
        let visibleLabels = this.getVisibleZl();
        if(visibleLabels.length === 3){
            if(!visibleLabels.includes("pm10")){
                return;
            }if(!visibleLabels.includes("pm2_5")){
                return;
            }if(!visibleLabels.includes("avg")){
                return;
            }

            // ToDo Draw lines for pm10

        }
        if(visibleLabels.length === 2){
            if(!visibleLabels.includes("pm10")){
                return;
            }if(!visibleLabels.includes("pm2_5")) {
                return;
            }
            // ToDo Draw lines for pm 10
        }

        if(visibleLabels.length === 1){
            let zl = visibleLabels[0];
            // ToDo Draw lines for zl
        }

        // limits are in this.limits

    }

    /***
     * Get array of selected zl
     *
     * @returns array - array of names of zl that are still selected on chart
     */

    getVisibleZl(){
        let result = []
        for(let i = 0; i < this.zl.length; i++){
            if(this.chart.isDatasetVisible(i)){
                result.push(this.zl[i]["name"]);
            }
        }
        return result;
    }

    getZlIndex(name){
        for(let i = 0; i < this.zl.length; i++){
            if(this.zl[i].name === name){
                return i;
            }
        }
        return -1;
    }

    addAverageValue(stationName, hour, value){
        let i = this.getZlIndex("avg");
        this.zl[i].addValue(stationName, hour, value)
    }


    removeAverageValue(stationName, hour){
        let i = this.getZlIndex("avg");
        this.zl[i].remove(stationName, hour);
    }

}