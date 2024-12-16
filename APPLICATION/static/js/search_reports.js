function searchTable(url) {
    // Obtener los valores de los filtros
    const filterUserValue = document.getElementById('filterUser') ? document.getElementById('filterUser').textContent.trim() : null;
    const filterCategoryValue = document.getElementById('filterCategory') ? document.getElementById('filterCategory').textContent.trim() : null;
    const dateRangeValue = document.getElementById('filterDateRange') ? document.getElementById('filterDateRange').value : null;

    // Crear el objeto de datos a enviar
    let data = {
        'dateRange': dateRangeValue,
        'user': filterUserValue,
        'category': filterCategoryValue
    };

    // Enviar la petición AJAX
    $.ajax({
        url: url,
        data: data,
        method: 'GET',
        success: function(response) {
            // Actualizar la tabla
            $('.table__body').html(response.body);
            $('.table__footer').html(response.footer);

            // Actualizar el gráfico
            updateChart(response.categories, response.data);
        },
        error: function(error) {
            console.error("Error en la petición AJAX:", error);
        }
    });
}

function updateChart(categories, data) {
    var options = {
        series: [
            { name: 'Intervenciones', data: data['intervenciones'] },
            { name: 'Mantenimientos', data: data['mantenimientos'] },
            { name: 'Cambios de parte', data: data['cambios de parte'] }
        ],
        chart: {
            type: 'line',
            height: 350
        },
        xaxis: {
            categories: categories
        }
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
}

const viewReports = document.getElementById("viewReports");
if (viewReports) {
    // Establecer el filtro de rango de fechas
    const filterDateRange = document.getElementById('filterDateRange');
    $(filterDateRange).on('apply.daterangepicker', function (ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
        searchTable('/view_reports/');
    });

    // Observar cambios en el filtro de usuario
    const filterUser = document.getElementById('filterUser');
    if (filterUser) {
        const observer = new MutationObserver(() => searchTable('/view_reports/'));
        observer.observe(filterUser, { childList: true, subtree: true });
    }

    // Observar cambios en el filtro de categoría
    const filterCategory = document.getElementById('filterCategory');
    if (filterCategory) {
        const observer = new MutationObserver(() => searchTable('/view_reports/'));
        observer.observe(filterCategory, { childList: true, subtree: true });
    }
}
