function drawTotalRainfall(graphDetails) {
    Highcharts.chart('totalRainfallGraph', {
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: null
        },
        xAxis: [{
            categories: graphDetails.time_list,
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            title: {
                text: 'Hourly Rainfall (inches)',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: 'Cumulative Rainfall (inches)',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        legend: {
            layout: 'vertical',
            align: 'top',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: false,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
            name: 'Hourly',
            type: 'column',
            yAxis: 1,
            data: graphDetails.hourly_rainfall,
            tooltip: {
                valueSuffix: ' inches'
            }

        }, {
            name: 'Cumulative',
            type: 'spline',
            data: graphDetails.cumulative_rain,
            tooltip: {
                valueSuffix: ' inches'
            }
        }]
    });
}
