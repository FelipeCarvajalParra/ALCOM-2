// Extensiones de Day.js para soporte de formato y manipulación
dayjs.extend(window.dayjs_plugin_localeData);
dayjs.extend(window.dayjs_plugin_utc);
dayjs.locale('es');

const calendarContainer = document.getElementById('ex-ghDay');
const legendContainer = document.getElementById('ex-ghDay-legend');
const container = document.getElementById('container__heatmap');
const user_id = document.getElementById('idUserAccount').getAttribute('data-user');

// Mantener una referencia única para el listener de clic
let dayClickListener = null;

function sendRequest(date) {
    let data = { date: date };

    return $.ajax({
        url: `/edit_user/${user_id}`, // Ruta que devuelve solo las intervenciones
        data: data,
        method: 'GET',
    })
    .then(response => {
        // Verifica si la respuesta contiene la clave 'body' y si es válida
        if (response.body) {
            // Actualizar solo la lista de intervenciones
            $('.container__interventions-list').html(response.body);
        }
    })
    .catch(error => {
        console.error("Request error:", error);
    });
}

// Función para inicializar o actualizar el mapa de calor
function updateHeatmap(year) {
    calendarContainer.innerHTML = ''; // Limpiar el contenedor del mapa
    legendContainer.innerHTML = ''; // Limpiar la leyenda

    const filteredData = interventionsData.filter(d => d.date.startsWith(year.toString()));
    const containerWidth = container.clientWidth;
    const cellWidth = containerWidth / 60;

    const cal = new CalHeatmap();
    window.miVariableGlobal = cal; // Mantener referencia global para futuras actualizaciones

    // Crear el nuevo mapa de calor
    cal.paint({
        date: { 
            start: new Date(`${year}-01-01`),
            locale: 'es'
         },
        data: {
            source: filteredData,
            type: 'json',
            x: 'date',
            y: (d) => +d['interventions'],
            groupY: 'max',
        },
        range: 1,
        scale: {
            color: {
                type: 'threshold',
                range: ['#e0f2ff', '#b3d9f7', '#80b8f1', '#5097d3', '#1a7bbf'], 
                domain: [2, 4, 6, 8], 
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
                        const dateText = dayjsDate.locale('es').format('LL'); // Asegúrate de que 'es' esté configurado aquí
                        const interventionText = value
                            ? `${value} Intervención${value > 1 ? 'es' : ''}`
                            : '0 Intervenciones';
                        return `${interventionText} el ${dateText}`;
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
                sendRequest(formattedDate);
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

    const months = dayjs.monthsShort();
    months.forEach((month) => {
        const monthLabel = document.createElement('div');
        
        monthLabel.textContent = month.charAt(0).toUpperCase() + month.slice(1);
        
        monthLabel.style.textAlign = 'center';
        monthLabels.appendChild(monthLabel);
    });

    calendarContainer.parentElement.insertBefore(monthLabels, calendarContainer);
}


// Inicialización al cargar la página
window.onload = function () {
    const currentYear = new Date().getFullYear();
    generateMonthLabels(); // Generar etiquetas de los meses
    updateHeatmap(currentYear); // Mostrar el mapa inicial con el año actual

    // Listener para cambiar el año seleccionado
    const yearSelect = document.getElementById('yearSelect');
    yearSelect.addEventListener('change', function () {
        const selectedYear = yearSelect.value;
        updateHeatmap(selectedYear); // Actualizar el mapa de calor con el nuevo año
    });
};
