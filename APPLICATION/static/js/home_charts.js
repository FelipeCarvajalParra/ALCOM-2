document.getElementById('TotalInterventions').innerText = dataLineChart.metrics.total_intervention;
document.getElementById('monthInterventionsCount').innerText = dataLineChart.metrics.month_interventions_count;
document.getElementById('weekInterventionsCount').innerText = dataLineChart.metrics.week_interventions_count;
document.getElementById('userGoal').innerText = dataLineChart.metrics.goal;

$.getJSON('https://cdn.jsdelivr.net/npm/apexcharts/dist/locales/es.json', function (data) {
    var es = data;

    // Opciones de la gráfica
    var options = {
        series: dataLineChart.graph.series,
        chart: {
            type: 'bar',
            height: 350,
            stacked: true,
            toolbar: { show: true },
            zoom: { enabled: true },
            locales: [es],  // Asignar la localización cargada
            defaultLocale: 'es'  // Establecer idioma en español
        },
        responsive: [{
            breakpoint: 480,
            options: { legend: { position: 'bottom', offsetX: -10, offsetY: 0 } }
        }],
        plotOptions: {
            bar: {
                horizontal: false,
                borderRadius: 10,
                dataLabels: {
                    total: { enabled: true, style: { fontSize: '13px', fontWeight: 900 } }
                }
            },
        },
        xaxis: {
            type: 'datetime',
            categories: dataLineChart.graph.categories
        },
        legend: { position: 'right', offsetY: 40 },
        fill: { opacity: 1 }
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
});


var options = {
    series: [dataLineChart.metrics.percentage],
    chart: {
        height: 350,
        type: 'radialBar',
    },
    plotOptions: {
        radialBar: {
            hollow: {
                size: '70%',
            }
        },
    },
    labels: ['Meta semanal'],
};

var chart = new ApexCharts(document.querySelector("#radialChart"), options);
chart.render();










    // Obtener las categorías y las series del JSON
    const categories = chartLineData.categories;
    const seriesData = chartLineData.series;
    const range = chartLineData.range;

    // Organizar las series
    const series = seriesData
        .filter(seriesItem => seriesItem.name && Array.isArray(seriesItem.data))
        .map(seriesItem => {
            return {
                name: seriesItem.name,
                data: seriesItem.data,
            };
        });

    // Asegurarnos de que el contenedor #chartLine existe en el DOM
    const chartContainer = document.querySelector("#lineChart");

    var options = {
        series: series, // Usar las series organizadas desde el JSON
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            width: [5, 7, 5],
            curve: 'straight',
            dashArray: [0, 0, 0]  // Cambiar a 0 para todas las líneas
        },
        title: {
            text: range,
            align: 'left'
        },
        legend: {
            tooltipHoverFormatter: function (val, opts) {
                return val + ' - <strong>' + opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] + '</strong>';
            }
        },
        markers: {
            size: 0,
            hover: {
                sizeOffset: 6
            }
        },
        xaxis: {
            categories: categories,
            convertedCatToNumeric: true,
        },
        tooltip: {
            y: [
                {
                    title: {
                        formatter: function (val) {
                            return val;
                        }
                    }
                },
                {
                    title: {
                        formatter: function (val) {
                            return val;
                        }
                    }
                },
                {
                    title: {
                        formatter: function (val) {
                            return val;
                        }
                    }
                }
            ]
        },
        grid: {
            borderColor: '#f1f1f1',
        }
    };

    
    
    window.chart = new ApexCharts(chartContainer, options);
    window.chart.render();
    