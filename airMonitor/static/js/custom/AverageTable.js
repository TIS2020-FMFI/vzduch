class AverageTable {
    constructor(data) {
        this.data = data;
        this.station = null;
        this.hourly_values = this.data['hours'];
        this.average_values = this.data['averages'];

    }

    setStation(station) {
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
        return this.station !== null ? tmp.slice(tmp.length - 13, tmp.length) : [];
    }

    getAverageValues() {
        let tmp = this.average_values[this.station];
        return this.station !== null ? tmp.slice(tmp.length - 13, tmp.length) : [];
    }

    updateTable(station_id) {
        this.setStation(station_id);
        hourly_values = this.getHourValues();
        average_values = this.getAverageValues();

        let rows = document.getElementsByClassName('valueRows');

        for (let i = 0; i < (rows[0].children.length - 1); i++) {
            if (i > 12) {
                rows[0].children[i + 1].children[0].value = '';
                rows[1].children[i + 1].children[0].value = '';
            } else {
                rows[0].children[i + 1].innerHTML =
                    hourly_values[i] !== null ? hourly_values[i].toFixed(1) : '';
                rows[1].children[i + 1].innerHTML =
                    average_values[i] !== null ? average_values[i].toFixed(1) : '';
            }
        }
    }

    getTable() {
        let table = document.createElement('table');
        table.style.width = '1%';
        table.classList.add('table');

        let header = document.createElement('thead');
        let headerRow = document.createElement('tr');
        let headerCell = document.createElement('th');
        headerCell.style.border = '1px solid black';
        headerCell.style.textAlign = 'center';
        headerCell.style.fontSize = '25px';
        headerCell.colSpan = "19";
        headerCell.appendChild(document.createTextNode('12-h Moving average PM10'));

        headerRow.appendChild(headerCell);
        header.appendChild(headerRow);
        table.appendChild(header);

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
                    td.style.width = '70px';
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

                if (i === 0) {
                    td.appendChild(document.createTextNode(hourly_values[j] !== null ? hourly_values[j].toFixed(1) : ''));
                } else {
                    td.appendChild(document.createTextNode(average_values[j] !== null ? average_values[j].toFixed(1) : ''));
                }
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
        }

        table.appendChild(thead);
        table.appendChild(tbody);

        return table;
    }

}