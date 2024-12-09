// Extensiones de Day.js para soporte de formato y manipulación
dayjs.extend(window.dayjs_plugin_localeData);
dayjs.extend(window.dayjs_plugin_utc);

const searchYearInterventions = document.getElementById('searchYearInterventions');
const calendarContainer = document.getElementById('ex-ghDay');
const legendContainer = document.getElementById('ex-ghDay-legend');
const container = document.getElementById('container__heatmap');
let selectedYear = searchYearInterventions.value || new Date().getFullYear(); // Año inicial
const user_id = document.getElementById('idUserAccount').getAttribute('data-user');

// Mantener una referencia única para el listener de clic
let dayClickListener = null;

function sendRequest(year, date = null) {
    let data = { year: year, date: date };

    return $.ajax({
        url: `/edit_user/${user_id}`,
        data: data,
        method: 'GET',
    })
    .then(response => {
        console.log("Request sent:", response);

        // Actualizar el contenedor con la respuesta
        $('.container__healt-map').html(response.body);

        // Reinicializar el mapa de calor
        updateHeatmap(selectedYear);
        console.log("Heatmap updated");
    })
    .catch(error => {
        console.error("Request error:", error);
    });
}

// Función para inicializar o actualizar el mapa de calor
function updateHeatmap(year) {
    console.log('Updating heatmap for year:', year);
    calendarContainer.innerHTML = ''; // Limpiar el contenedor del mapa
    legendContainer.innerHTML = ''; // Limpiar la leyenda

    const filteredData = interventionsData.filter(d => d.date.startsWith(year.toString()));
    const containerWidth = container.clientWidth;
    const cellWidth = containerWidth / 60;

    const cal = new CalHeatmap();
    
    // Asegurarse de destruir cualquier instancia anterior del mapa
    cal.destroy();

    // Crear el nuevo mapa de calor
    cal.paint({
        data: {
            source: filteredData,
            type: 'json',
            x: 'date',
            y: (d) => +d['interventions'],
            groupY: 'max',
        },
        date: { start: new Date(`${year}-01-01`) },
        range: 1,
        scale: {
            color: {
                type: 'threshold',
                range: ['#e0f2ff', '#b3d9f7', '#80b8f1', '#5097d3', '#1a7bbf'],
                domain: [1, 3, 5, 7, 10],
            },
        },
        domain: {
            type: 'year',
            label: { text: null },
            width: '100%',
        },
        subDomain: {
            type: 'day',
            radius: 2,
            width: cellWidth,
            height: cellWidth,
        },
        itemSelector: '#ex-ghDay',
    }, [
        [
            Tooltip,
            {
                text: function (date, value, dayjsDate) {
                    return (
                        (value ? value + ' Intervenciones' : '0 Intervenciones') +
                        ' el ' +
                        dayjsDate.format('LL')
                    );
                },
            },
        ],
        [
            LegendLite,
            {
                includeBlank: true,
                itemSelector: '#ex-ghDay-legend',
                radius: 2,
                width: cellWidth,
                height: cellWidth,
                gutter: 4,
            },
        ],
    ]);

    // Eliminar cualquier listener de clic anterior y agregar uno nuevo
    if (dayClickListener) {
        calendarContainer.removeEventListener('click', dayClickListener);
    }

    // Listener de clic actualizado
    dayClickListener = function (event) {
        const clickedElement = event.target.closest('rect');
        if (clickedElement && clickedElement.__data__) {
            const timestampDate = clickedElement.__data__.t;
            const clickedDate = dayjs(timestampDate).add(1, 'day');
            const formattedDate = clickedDate.format('DD/MM/YYYY'); // Formato solicitado

            // Buscar número de intervenciones para esa fecha
            const interventions = filteredData.find(
                (d) => d.date === clickedDate.format('YYYY-MM-DD'),
            )?.interventions;

            if (interventions) {
                sendRequest(selectedYear, formattedDate);
            }
        }
    };

    calendarContainer.addEventListener('click', dayClickListener);
}

// Generar etiquetas de los meses
function generateMonthLabels() {
    const monthLabels = document.createElement('div');
    monthLabels.style.display = 'grid';
    monthLabels.style.gridTemplateColumns = 'repeat(12, 1fr)';
    monthLabels.style.width = '100%';
    monthLabels.style.marginBottom = '8px';

    const months = dayjs.monthsShort(); // Abreviaturas de los meses
    months.forEach((month) => {
        const monthLabel = document.createElement('div');
        monthLabel.textContent = month;
        monthLabel.style.textAlign = 'center';
        monthLabels.appendChild(monthLabel);
    });

    calendarContainer.parentElement.insertBefore(monthLabels, calendarContainer);
}

// Evento para actualizar el mapa cuando cambia el año
searchYearInterventions.addEventListener('change', function () {
    const year = parseInt(searchYearInterventions.value, 10);
    if (!isNaN(year)) {
        selectedYear = year;
        updateHeatmap(selectedYear);

        // Enviar el año seleccionado
        sendRequest(selectedYear);
    }
});

// Inicialización al cargar la página
window.onload = function () {
    generateMonthLabels(); // Generar etiquetas de los meses
    updateHeatmap(selectedYear); // Mostrar el mapa inicial con el año por defecto
};
