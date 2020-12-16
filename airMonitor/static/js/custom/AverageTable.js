class AverageTable{
    constructor(data) {
        this.data = data;
        this.station = null;
        this.hourly_values = this.data['hours'];
        this.average_values = this.data['averages'];

    }

    setStation(station) {
        console.log(station);
        this.station = station;
    }

    getStation() {
        return this.station;
    }

    getData() {
        return this.data;
    }

    getHourValues() {
        let tmp = this.hourly_values[this.station];
        return this.station !== null ? tmp.slice(tmp.length-13, tmp.length) : [];
    }

    getAverageValues() {
        let tmp = this.average_values[this.station];
        return this.station !== null ? tmp.slice(tmp.length-13, tmp.length) : [];
    }

    // countAverage() {
    //     for (const key in this.data) {
    //
    //         this.average_values[key] = [];
    //
    //         let len = this.data[key].length;
    //         let tmp_arr = this.data[key].slice(len-12, len);
    //         for (let i = len-12; i >= 0; i--) {
    //             this.average_values[key].unshift(this.average(tmp_arr));
    //             tmp_arr.pop();
    //             tmp_arr.unshift(this.data[key][i-1]);
    //         }
    //
    //     }
    //     console.log('averages', this.average_values.length);
    // }


    // average(values) {
    //     let sum = 0;
    //     for (let i = 0; i < values.length; i ++) {
    //         if (values[i] !== null) {
    //             sum += values[i];
    //         }
    //     }
    //     return sum !== 0 ? (sum/values.length).toFixed(3) : null;
    // }



    updateTable(station_id) {
        this.setStation(station_id);
        hourly_values = this.getHourValues();
        average_values =  this.getAverageValues();

        let rows = document.getElementsByClassName('valueRows');

        for (let i = 0; i < (rows[0].children.length-1); i++) {
            if (i > 12) {
                rows[0].children[i+1].children[0].value = '';
                rows[1].children[i+1].children[0].value = '';
            } else {
                rows[0].children[i+1].innerHTML =
                    hourly_values[i] !== -1 ? hourly_values[i].toFixed(3) : '';
                rows[1].children[i+1].innerHTML = average_values[i].toFixed(3);
            }
        }

    }

    getTable() {
        let table = document.createElement('table');
        table.style.width = '50%';
        table.classList.add('table');

        let thead = document.createElement('thead');
        let headRow = document.createElement('tr');
        let columnNames = ["-12h", "-11h", "-10h", "-9h", "-8h", "-7h",
            "-6h", "-5h", "-4h", "-3h", "-2h", "-1h",
            "0h", "+1h", "+2h", "+3h", "+4h", "+5h",];

        let th = document.createElement('th');
        th.appendChild(document.createTextNode(''));
        th.style.border = '1px solid black';
        headRow.appendChild(th);

        for (let i = 0; i < 18; i++) {
            let th = document.createElement('th');
            th.appendChild(document.createTextNode(columnNames[i]));
            th.style.border = '1px solid black';
            headRow.appendChild(th);
        }

        thead.appendChild(headRow);

        let tbody = document.createElement('tbody');

        for (let i = 0; i < 2; i++) {
            let tr = document.createElement('tr');
            tr.classList.add('valueRows');
            let td = document.createElement('td');
            td.appendChild(document.createTextNode(i === 0 ? "HOUR" : "AVG"));
            td.classList.add('nullCell');
            td.style.border = '1px solid black';
            td.style.width = '50px';
            tr.appendChild(td);


            for (let j = 0; j < 18; j++) {
                let td = document.createElement('td');
                td.style.border = '1px solid black';
                td.style.width = '50px';
                td.classList.add('valueCell');

                if (j > 12) {
                    td.classList.add("input");
                    td.style.padding = '0';
                    let input = document.createElement('input');
                    input.id = i === 0 ? 'hour_' + (j - 12) + 'h' : 'avg_' + (j - 12) + 'h';
                    input.type = "text";
                    input.disabled = i !== 0;
                    input.style.width = '100%';
                    input.style.height = '37px';
                    td.appendChild(input);
                    tr.appendChild(td);
                    continue;
                }

                 if ( i === 0 ) {
                    td.appendChild(document.createTextNode(hourly_values[j] !== null ? hourly_values[j].toFixed(3) : ''));
                } else {
                    td.appendChild(document.createTextNode(average_values[j] !== null ? average_values[j].toFixed(3) : ''));
                }
                td.style.border = '1px solid black';
                td.style.width = '50px';
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        table.appendChild(thead);
        table.appendChild(tbody);

        return table;
    }

}