/***
 *  Listener for changes of station
 */
document.getElementById("id_stations").onchange = function (){
     let sel = document.getElementById('id_stations');
     let opt = sel.options[sel.selectedIndex];
     chart.setStation(opt.text);
     chart.updateChart();
     avgTable.updateTable(opt.text);

};

/***
 * Listener for changes of days
 */
document.getElementById("id_days").onchange = function (){
     let sel = document.getElementById('id_days');
     let opt = sel.options[sel.selectedIndex];
     chart.setDays(opt.text);
     chart.updateChart();
};

/***
 * Listeners for selecting of graph type
 */
document.getElementById("noLines").onclick = function (){
    chart.showLine(false);
    chart.updateChart();
};
document.getElementById("withTension").onclick = function (){
    chart.showTension(true);
    chart.drawChart();
};
document.getElementById("withoutTension").onclick = function (){
    chart.showTension(false);
    chart.drawChart();
};

/***
 * Event on load of window
 */
window.onload = function() {
    let sel = document.getElementById('id_stations');
    let opt = sel.options[sel.selectedIndex];
    chart.setStation(opt.text);
    sel = document.getElementById('id_days');
    opt = sel.options[sel.selectedIndex];
    chart.setDays(opt.text);
    chart.drawChart();
};


window.addEventListener('load', (e) => {
    let added_values = [NaN, NaN, NaN, NaN, NaN];
    for (let i = 1; i <= 5; i++) {
        let tmp = document.getElementById('hour_' + i + 'h');
        tmp.addEventListener('input', (ev) => {
            added_values[i - 1] = (isNumber(tmp.value)) ? parseFloat(tmp.value) : NaN;
            for (let k = 1; k <= 5; k++) {
                if (!isNaN(added_values[k - 1])) {
                    let nums = added_values.slice(0, k).filter(n => !isNaN(n));
                    let avg = average(nums.concat(hourly_values.slice(nums.length + 1, hourly_values.length)));
                    document.getElementById('avg_' + k + 'h').value = avg;

                    chart.addValue(chart.stationName, k - 1, 'avg', avg);
                    chart.addValue(chart.stationName, k - 1, 'pm10', nums[k-1]);
                    chart.updateChart();
                } else {
                    document.getElementById('hour_' + k + 'h').value = '';
                    document.getElementById('avg_' + k + 'h').value = '';

                    chart.removeValue(chart.stationName, k - 1, 'avg');
                    chart.removeValue(chart.stationName, k - 1, 'pm10');
                    chart.updateChart();
                }
            }
        });
    }
}, false);

 function average(vals) {
    let total = 0;
    for (let i = 0; i < vals.length; i++) {
        if (vals[i] !== -1) {
            total += vals[i];
        }

    }
    total = total / vals.length;
    return total.toFixed(1);
}

function isNumber(value) {
    return /[+-]?([0-9]*[.])?[0-9]+/.test(value);
}
