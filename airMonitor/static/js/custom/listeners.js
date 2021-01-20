/***
 *  Listener for changes of station
 */
document.getElementById("id_stations").onchange = function (){
     let sel = document.getElementById('id_stations');
     let opt = sel.options[sel.selectedIndex];
     chart.setStation(opt.text);
     chart.updateChart();
     avgTable.updateTable(opt.text);

}

/***
 * Listener for changes of days
 */
document.getElementById("id_days").onchange = function (){
     let sel = document.getElementById('id_days');
     let opt = sel.options[sel.selectedIndex];
     chart.setDays(opt.text);
     chart.updateChart();
}

/***
 * Listeners for selecting of graph type
 */
document.getElementById("noLines").onclick = function (){
    chart.showLine(false);
    chart.updateChart();
}
document.getElementById("withTension").onclick = function (){
    chart.showTension(true);
    chart.drawChart();
}
document.getElementById("withoutTension").onclick = function (){
    chart.showTension(false);
    chart.drawChart();
}


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