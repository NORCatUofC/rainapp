function drawTotalRainfall(floodingData) {
    $('#floodingGraph').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Basement Flooding Reported'
        },
        subtitle: {
            text: 'Source: <a href="#">311</a>'
        },
        xAxis: {
            categories: floodingData.dates,
            title: {
                text: 'Households reported'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Ward'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' houses'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 80,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Wards',
            data: graphData.wards
        }]
    });
}
