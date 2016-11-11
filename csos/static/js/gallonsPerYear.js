function showCounter(total, counterStart) {

    var totalStart = (total - counterStart).toLocaleString();

    $('#theCounter').addClass('counter-analog').counter({
        initial: totalStart,
        direction: 'up',
        interval: '1',
        format: total.toLocaleString(),
        stop: total.toLocaleString()
    });
}

// High charts

function drawGallonsPerYearChart(events) {
    $('#gallonsPerYearChart').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Sewage Dumped per Year'
        },
        xAxis: {
            categories: events.years
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Millions of Gallons'
            }
        },
        legend: {
            reversed: true
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        series: events.series
    });

}