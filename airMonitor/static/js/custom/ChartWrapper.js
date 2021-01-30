class ChartWrapper {
    constructor(data) {
        this.data = data;

        // Set limits for all pollutant
        this.limits = data["limits"];
        data["limits"] = null;
        this.metas = [];

        // Create all pollutant and push them into pollutant array
        this.pollutants = [];
        for (let k in data["data"]["datasets"]) {
            let d = data["data"]["datasets"][k];
            this.pollutants.push(new Pollutants(d["label"], d["data"], d["fill"], d["backgroundColor"]));
            if(d["label"] === "pm10" || d["label"] === "pm2_5" || d["label"] === "12-hour" || d["label"] === "24-hour"){
                this.metas.push(null);
            }
            else {
                 this.metas.push(true);
             }
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
        this.data["options"]["horizontalLine"] = null;

        this.data["options"]["scales"]["yAxes"][0]["ticks"] = {
            callback: function(value, index, values) {
                        return value + "\u00B5g/m3";
                    }
        };



        // Plugin to print out horizontal lines
        this.horizonalLinePlugin = {
            afterDraw: function(chartInstance) {
                let yScale = chartInstance.scales["y-axis-0"];
                let canvas = chartInstance.chart;
                let ctx = canvas.ctx;
                let index;
                let line;
                let style;
                let yValue;

                if (chartInstance.options.horizontalLine) {
                  for (index = 0; index < chartInstance.options.horizontalLine.length; index++) {
                    line = chartInstance.options.horizontalLine[index];

                    style = line.style;
                    yValue = yScale.getPixelForValue(line.y);
                    if(yValue < 50){
                        continue;
                    }
                    if(yValue > 515){
                        continue;
                    }

                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    for(let i = 50; i <= canvas.width; i += 10){
                        if((i / 10) % 2  === 1){
                            ctx.moveTo(i, yValue);
                        }
                        else{
                            ctx.lineTo(i, yValue);
                        }
                    }
                    ctx.strokeStyle = style;
                    ctx.stroke();
                  }
                }
              }
            };
        Chart.pluginService.register(this.horizonalLinePlugin);


        // ChartJs item
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.chart = new Chart(this.ctx, this.data);
        this.setLimits("pm10");
    }

    getChart() {
        this.updateChart();
        return this.chart;
    }

    setStation(station) {
        this.stationName = station;
    }

    setDays(days) {
        this.days = days;
        this.setHours();
    }

    setHours() {
        this.hours = this.days * 24;
    }

    drawChart() {
        this.getChart();
        window.myLine = this.chart;
    }

    /***
     *  Function that collect all data and updated chart according to them
     */
    updateChart() {
        let dataset = [];
        for (let z in this.pollutants) {
            let data;
            data = this.pollutants[z].get(this.stationName, this.hours);
            if (!this.show_line) {
                data["showLine"] = this.show_line;
            }
            dataset.push(data);
        }
        this.data["data"]["datasets"] = dataset;
        if (this.hours - 6 > this.labels.length) {
            this.data["data"]["labels"] = this.labels;
        } else {
            this.data["data"]["labels"] = this.labels.slice(this.labels.length - this.hours - 6,
                this.labels.length);
        }

        if (this.tension) {
            this.data["options"]["elements"]["line"]["tension"] = 0.5;
        } else {
            this.data["options"]["elements"]["line"]["tension"] = 0;
        }
        for(let index = 0; index < this.metas.length; index++){
            let ci = this.chart.chart;
            let meta = ci.getDatasetMeta(index);
            meta.hidden = meta.hidden === null ? this.metas[index] : null;
        }
        this.chart.update({
            "lazy": true,
            "duration": 0,
        })
    }

    /***
     * @param show - boolean that says whether to show lines or not
     */

    showLine(show) {
        this.show_line = show;
    }

    /***
     * @param show - boolean that says whether to show tension or not
     */

    showTension(show) {
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
        chart.metas[index] = meta.hidden;

        if (this.chart.getVisibleDatasetCount() <= 4) {
            chart.processLabels();
        }
        else{
            chart.data.options.horizontalLine = null;
        }

        ci.update({
            "duration": 0,
            "lazy": true,
        });
    }

    /***
     *
     *  Function for processing which pollutant are selected and draw lines depending on their limits
     *
     */

    processLabels() {
        let visibleLabels = this.getVisiblePollutants();
        if (visibleLabels.length === 4) {
            if (!visibleLabels.includes("pm10") || !visibleLabels.includes("pm2_5") || !visibleLabels.includes("12-hour") || !visibleLabels.includes("24-hour")) {
                chart.data.options.horizontalLine = null;
                return;
            }
            this.setLimits("pm10");
            return;
        }
        if (visibleLabels.length === 3) {
            if (!visibleLabels.includes("pm10") || !visibleLabels.includes("pm2_5") || !(visibleLabels.includes("12-hour") || visibleLabels.includes("24-hour"))) {
                chart.data.options.horizontalLine = null;
                return;
            }
            this.setLimits("pm10");
            return;
        }
        if (visibleLabels.length === 2) {
            if (!visibleLabels.includes("pm10") && !visibleLabels.includes("pm2_5")) {
                chart.data.options.horizontalLine = null;
                return;
            }
            if (!visibleLabels.includes("pm10") && !(visibleLabels.includes("12-hour") || visibleLabels.includes("24-hour"))) {
                chart.data.options.horizontalLine = null;
                return;
            }
            if (!(visibleLabels.includes("12-hour") || visibleLabels.includes("24-hour")) && !visibleLabels.includes("pm2_5")) {
                chart.data.options.horizontalLine = null;
                return;
            }
            this.setLimits("pm10");
            return;
        }

        if (visibleLabels.length === 1) {
            let pollutant = visibleLabels[0];
            if(pollutant === "24-hour" || pollutant === "12-hour"){
                pollutant = "pm10";
            }
            this.setLimits(pollutant);
        }

    }

    setLimits(pollutant){
        this.data.options.horizontalLine = [{
                "y": this.limits[pollutant]["4"],
                "style": "rgba(255, 0, 0, .4)"
            }, {
                "y": this.limits[pollutant]["3"],
                "style": "rgba(255, 192, 0, .4)"
            }, {
                "y": this.limits[pollutant]["2"],
                "style": "rgba(255, 255, 0, .4)"
            }, {
                "y": this.limits[pollutant]["1"],
                "style": "rgba(146, 208, 80, .4)"
            }];
    }

    /***
     * Get array of selected pollutant
     *
     * @returns array - array of names of pollutant that are still selected on chart
     */

    getVisiblePollutants() {
        let result = [];
        for (let i = 0; i < this.pollutants.length; i++) {
            if (this.chart.isDatasetVisible(i)) {
                result.push(this.pollutants[i]["name"]);
            }
        }
        return result;
    }

    getPollutantIndex(name) {
        for (let i = 0; i < this.pollutants.length; i++) {
            if (this.pollutants[i].name === name) {
                return i;
            }
        }
        return -1;
    }

    addValue(stationName, hour, pollutant, value) {
        let i = this.getPollutantIndex(pollutant);
        this.pollutants[i].addValue(stationName, hour, value)
    }

    removeValue(stationName, hour, pollutant) {
        let i = this.getPollutantIndex(pollutant);
        this.pollutants[i].remove(stationName, hour);
    }

    getValue(station, pollutant, hour){
        for(let i = 0; i < this.pollutants.length; i++){
            if(this.pollutants[i].name === pollutant){
                return this.pollutants[i].getValue(station, hour);
            }
        }
    }
    getPollutantLevel(pollutant, value){
        if(value === null){
            return 0;
        }
        for(let i = 4; i > 0; i--){
            if(value > this.limits[pollutant][i.toString()]){
                return i + 1;
            }
        }
        return 1;
    }

}