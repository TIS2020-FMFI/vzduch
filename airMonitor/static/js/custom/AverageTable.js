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

}