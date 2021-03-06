var thresholds = {};

function setupChart(argThresholds){
    thresholds = argThresholds;
}

function drawNYearChart(recurrenceIntervals, initialDurations) {
    Highcharts.chart('nYearInteractive', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'How fast rain must fall to have an n-year event'
        },
        xAxis: {
            categories: recurrenceIntervals,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Rain Duration (hrs)'
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} hours</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        if (this.y > 1) {
                            return this.y + ' hours';
                        }
                        else if (this.y == 1) {
                            return '1 hour';
                        }
                        else if (inches < thresholds.boundaries[this.x][1]) {
                            return "Not enough rain";
                        }
                        else if (inches > thresholds.boundaries[this.x][240]) {
                            return "Less than 1 hour";
                        }
                        return 'Uh oh';
                    }
                }
            }
        },
        series: [{
            name: 'Rain Duration',
            data: initialDurations
        }],
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        }
    });
}

function stormsForInches(inchesArg) {

    inches = inchesArg;
    var removeThis = true;
    var retVal = [];
    for (var recurrence in thresholds.recurrence_intervals) {
        var recurrence_interval = thresholds.recurrence_intervals[recurrence];
        var threshold_boundaries = thresholds['boundaries'][recurrence_interval];

        var duration = 0;
        // var valueAdded = false;
        for (var duration_idx in thresholds.durations) {
            var duration_hrs = thresholds.durations[duration_idx];
            var boundary_inches = threshold_boundaries[duration_hrs];
            if (inches > boundary_inches) {
                if (duration_idx == 0) {
                    duration = 0;
                }
                else {
                    var prev_duration_hrs = thresholds.durations[duration_idx - 1];
                    var a = (prev_duration_hrs - duration_hrs) /
                        (threshold_boundaries[prev_duration_hrs] - threshold_boundaries[duration_hrs]);
                    var b = duration_hrs - (a * threshold_boundaries[duration_hrs]);
                    duration = (a * inches) + b;
                    duration = duration.toFixed(2);
                }
                break;
            }
        }
        retVal.push(parseInt(duration));
    }
    return retVal;
}

function updateInches(newInches) {
    newInches = newInches.toFixed(2);
    var chartType = $(this)[0].id;
    var chart = $('#nYearInteractive').highcharts();
    chart.update({
        series: [{
            data: stormsForInches(newInches, thresholds)
        }],
        title: {
            text: 'How fast ' + newInches + ' inches of rain must fall to have an n-year event'
        }
    });

}