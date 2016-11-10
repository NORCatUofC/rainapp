function buildAndDisplayData(data) {
    var total = 0;

    for (var i = 0; i < data.length; i++) {
        total += parseFloat(data[i].total);
    }
    // Convert total to gallons (from millions of gallons) and an integer
    total = parseInt(total * 1000000)
    showCounter(total);
    var a = eventsSeries(data);;
    drawGallonsPerYearChart(a.years, a.series);

}

function showCounter(total) {

    var total_start = (total - 1000000).toLocaleString();

    $('#theCounter').addClass('counter-analog').counter({
        initial: total_start,
        direction: 'up',
        interval: '1',
        format: total.toLocaleString(),
        stop: total.toLocaleString()
    });
}

function eventsSeries(data) {
    var yearsList = [];
    var tracker = {
        crcw: [],
        wilmette: [],
        obrien: []
    }

    for (var i = 0; i < data.length; i++) {
        var event = data[i];
        
        yearsList.push(formatOverflowDates(event.start_date, event.end_date));
        tracker.crcw.push(parseFloat(event.crcw));
        tracker.wilmette.push(parseFloat(event.wilmette));
        tracker.obrien.push(parseFloat(event.obrien));
    }

    var series = [
        {
            name: 'Calumet',
            data: tracker.obrien
        },
        {
            name: 'Wilmette',
            data: tracker.wilmette
        },
        {
            name: 'Downtown',
            data: tracker.crcw
        }
    ];


    return {
        series: series,
        years: yearsList
    };

}

function gallonsPerStationSeries(data) {
    var yearsList = [2016];

    for (var i = 0; i < data.length; i++) {
        var year = parseInt(data[i].year);
        if ($.inArray(year, yearsList) < 0) {
            yearsList.push(year);
        }

    }

    var years = function (yearsList) {
        yearsRet = {};
        for (var y = 0; y < yearsList.length; y++) {
            yearsRet[yearsList[y]] = 0;
        }
        return yearsRet;
    }

    var stations = {
        crcw: {
            name: 'Downtown',
            years: years(yearsList)
        },
        obrien: {
            name: 'Calumette',
            years: years(yearsList)
        },
        wilmette: {
            name: 'Wilmette',
            years: years(yearsList)
        }
    };

    for (var i = 0; i < data.length; i++) {
        var event = data[i];
        stations['crcw']['years'][parseInt(event.year)] += parseFloat(event['crcw']);
        stations['obrien']['years'][parseInt(event.year)] += parseFloat(event['obrien']);
        stations['wilmette']['years'][parseInt(event.year)] += parseFloat(event['wilmette']);
    }

    retVal = [];
    $.each(stations, function (index, station) {
        series = {
            name: station.name,
            data: []
        };
        $.each(station.years, function (index, year) {
            series['data'].push(year);
        });
        series['data'].reverse()
        retVal.push(series);
    });

    return {
        series: retVal,
        years: yearsList
    };
}

function formatOverflowDates(startDate, endDate) {
    var startSplit = startDate.split('-');
    var retVal = startSplit[0] + "   " + startSplit[1] + "/" + startSplit[2];
    if (endDate != "") {
        var endSplit = endDate.split('-');
        retVal += " - " + endSplit[1] + "/" + endSplit[2];
    }
    return retVal;
    
}