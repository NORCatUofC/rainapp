// High charts



function drawGallonsPerYearChart(years, series) {
    $('#gallonsPerYearChart').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Sewage Dumped per Year'
        },
        xAxis: {
            categories: years
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
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        series: series
    });

}