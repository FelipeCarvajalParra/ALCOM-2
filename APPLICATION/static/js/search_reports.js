let currentAjaxRequest = null; // Variable para manejar la solicitud AJAX activa

// Función que realiza la petición AJAX
function petition(dateRange) {

    dateRange = dateRange || $('#filterDateRange').val();

    const filterUserElement = document.getElementById('filterUser');
    const filterUserValue = filterUserElement ? filterUserElement.textContent.trim() : null;

    const filterCategoryElement = document.getElementById('filterCategory');
    const filterCategoryValue = filterCategoryElement ? filterCategoryElement.textContent.trim() : null;

    let data = {
        'dateRange': dateRange,
        'filterUser': filterUserValue,
        'filterCategory': filterCategoryValue,
    };

    // Cancelar la solicitud anterior si existe
    if (currentAjaxRequest) {
        currentAjaxRequest.abort();
    }

    // Crear una nueva solicitud AJAX
    currentAjaxRequest = $.ajax({
        url: '/view_reports/',
        data: data,
        dataType: 'json', // Esperamos una respuesta en formato JSON
        method: 'GET',
    });

    // Manejar la respuesta
    return currentAjaxRequest.then(data => {
        updateChart(data);
    }).catch(error => {
        if (error.statusText !== "abort") { // Ignorar errores de abortar
            console.error('Error en la petición AJAX:', error);
        }
    }).always(() => {
        currentAjaxRequest = null; // Limpiar la solicitud activa después de completar
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

    // Actualizar el gráfico después de insertar el contenedor
    updateChart(interventionsByDay);
}

// Función para actualizar el gráfico
function updateChart(data) {

    // Obtener las categorías y las series del JSON
    const categories = data.categories;
    const seriesData = data.series;
    const range = data.range;

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

        // Verificar si el gráfico ya ha sido creado para actualizarlo, si no, crearlo
        if (window.chart) {
            window.chart.destroy();
            window.chart = new ApexCharts(chartContainer, options);
            window.chart.render();
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
        const rangeDate = picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD');

        // Realizar la petición con el nuevo rango de fechas
        petition(rangeDate);
    });
}

// Inicializar los datos al cargar la página
$(document).ready(function() {
    if (initialData) {
        updateChart(initialData);
    } else {
        const initialDateRange = $('#filterDateRange').val();
        if (initialDateRange) {
            petition(initialDateRange); // Realizar la petición inicial con el rango de fechas por defecto
        }
    }
});

const filterUser = document.getElementById('filterUser');
if (filterUser) {
    const observer = new MutationObserver(function(mutationsList) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'subtree') {
                petition();
            }
        }
    });

    observer.observe(filterUser, { childList: true, subtree: true });
}

const filterCategory = document.getElementById('filterCategory');
if (filterCategory) {
    const observer = new MutationObserver(function(mutationsList) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'subtree') {
                petition();
            }
        }
    });

    observer.observe(filterCategory, { childList: true, subtree: true });
}