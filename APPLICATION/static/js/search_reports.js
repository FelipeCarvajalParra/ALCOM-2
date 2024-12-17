// Función que realiza la petición AJAX
function petition(dateRange) {
    let data = {
        'dateRange': dateRange
    };

    // Realizar la petición AJAX al servidor
    return $.ajax({
        url: '/view_reports/',
        data: data,
        dataType: 'json', // Esperamos una respuesta en formato JSON
        method: 'GET'
    }).then(data => {
        console.log('Respuesta del servidor:', data);
        updateChart(data);
        
    }).catch(error => {
        console.error('Error en la petición AJAX:', error);
    });
}

// Función para actualizar la tabla de intervenciones
function updateInterventions(interventionsByDay) {
    let container = document.querySelector('.table__body');
    container.innerHTML = ''; // Limpiar contenido previo

    // Recorrer los datos de intervenciones por día
    for (let date in interventionsByDay) {
        let tasks = interventionsByDay[date];

        // Crear un nuevo div para cada día de intervenciones
        let div = document.createElement('div');
        div.classList.add('intervention-summary');
        div.innerHTML = `
            <h3>${date}</h3>
            <p>Intervenciones: ${tasks.Intervencion || 0}</p>
            <p>Cambio de parte: ${tasks["Cambio de parte"] || 0}</p>
            <p>Mantenimiento: ${tasks.Mantenimiento || 0}</p>
        `;
        container.appendChild(div);
    }

    // Si el contenedor del gráfico no existe, lo agregamos dinámicamente
    if (!document.querySelector("#chartLine")) {
        let chartContainer = document.createElement('div');
        chartContainer.id = "chartLine";
        container.appendChild(chartContainer);
    }

    // Actualizar el gráfico después de insertar el contenedor
    updateChart(interventionsByDay);
}




function updateChart(data) {

    console.log('Datos para el gráfico:', data);

    // Obtener las categorías y las series del JSON
    const categories = data.categories;
    const seriesData = data.series;

    // Organizar las series
    const series = seriesData.map(seriesItem => {
        return {
            name: seriesItem.name,
            data: seriesItem.data
        };
    });

    // Asegurarnos de que el contenedor #chartLine existe en el DOM
    const chartContainer = document.querySelector("#chartLine");

    // Verificar si el contenedor existe y renderizar el gráfico
    if (chartContainer) {
        let options = {
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
                text: 'Estadísticas de Intervenciones',
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
                categories: categories
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

        // Verificar si el gráfico ya ha sido creado para actualizarlo, si no, crearlo
        if (window.chart) {
            window.chart.updateOptions(options);
        } else {
            window.chart = new ApexCharts(chartContainer, options);
            window.chart.render();
        }
    } else {
        console.error('El contenedor del gráfico no se encuentra');
    }
}

// Función para manejar el rango de fechas del daterangepicker
const filterDateRange = document.getElementById('filterDateRange');
if (filterDateRange) {
    $(filterDateRange).on('apply.daterangepicker', function(ev, picker) {
        // Obtener el rango de fechas seleccionado
        const rangeDate = $(this).val();

        // Realizar la petición con el nuevo rango de fechas
        petition(rangeDate);
    });
}

$(document).ready(function() {
    // Si hay datos iniciales, actualizamos la tabla y el gráfico
    if (initialData) {
      
        console.log('Datos iniciales js:', initialData);

     
        updateChart(initialData);
    } else {
        // Si no hay datos iniciales, realizar la petición con el rango de fechas por defecto
        const initialDateRange = $('#filterDateRange').val();
        if (initialDateRange) {
            petition(initialDateRange); // Realizar la petición inicial con el rango de fechas por defecto
        }
    }
});