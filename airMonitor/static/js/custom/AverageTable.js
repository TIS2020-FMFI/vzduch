class AverageTable{
    constructor(data) {
        this.data = data;
        this.station = null;
        this.columnNames = ["-12h", "-11h", "-10h", "-9h", "-8h", "-7h",
            "-6h", "-5h", "-4h", "-3h", "-2h", "-1h",
            "0h", "+1h", "+2h", "+3h", "+4h", "+5h",];
    }

    setStation(station) {
        this.station = station;
    }

    getStation() {
        return this.station;
    }

    getHourValues() {
        return this.station !== null ? this.data["hours"][this.station] : [];
    }

    getAverageValues() {
        return this.station !== null ? this.data["averages"][this.station] : [];
    }

    updateTable(station_id) {
        let rows = document.getElementsByClassName('valueRows');
        console.log(station_id, typeof station_id);
        for (let i = 0; i < (rows[0].children.length-6); i++) {
            rows[0].children[i+1].innerHTML =
                this.data["hours"][station_id][12-i] !== -1 ? this.data["hours"][station_id][12-i] : '';
            rows[1].children[i+1].innerHTML = this.data["averages"][station_id][12-i];
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
                    td.appendChild(document.createTextNode(hourly_values[12 - j] !== -1 ? hourly_values[12 - j] : ''));
                } else {
                    td.appendChild(document.createTextNode(average_values[12 - j]));
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