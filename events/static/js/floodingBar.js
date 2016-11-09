var floodingData = {};

$(document).ready(function () {
    $('.switchBtn').on('click', function () {
        var chartType = $(this)[0].id;
        var chart = $('#floodingGraph').highcharts();
        chart.update({
            series: [{
                name: 'Cases Reported',
                data: floodingData[chartType].map(function (a) {
                    return a.count;
                })
            }],
            xAxis: {
                categories: floodingData[chartType].map(function (a) {
                    return a.label;
                }),
                title: {
                    text:  chartType.substr(0,1).toUpperCase()+chartType.substr(1)
                }
            }
        });
    })
});


function drawFloodingBar(floodingDataArg) {
    floodingData = floodingDataArg;
    $('#floodingGraph').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Basement Flooding Reported'
        },
        subtitle: {
            text: 'Source: <a href="#">311</a>'
        },
        xAxis: {
            categories: floodingData.wards.map(function (a) {
                return a.label;
            }),
            title: {
                text: 'Ward'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Flood cases reported'
            },
            labels: {
                overflow: 'justify'
            },
            step: 1
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
            data: floodingData.wards.map(function (a) {
                return a.count;
            })
        }]
    });
}
