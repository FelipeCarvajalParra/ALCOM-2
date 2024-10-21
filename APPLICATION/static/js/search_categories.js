

function searchCategories(page = 1) {
    var search = $('#searchCategories').val();

    $.ajax({
        url: '/view_categories/',
        data: {
            'search': search,
            'page': page // Enviar la página actual también
        },
        success: function(data) {
            // Actualizar el cuerpo de la tabla
            $('.table__body').html(data.body);
            // Actualizar el pie de la tabla
            $('.table__footer').html(data.footer);
        }
    });
}

// Manejar la búsqueda con debounce
let timeout;
$('#searchCategories').on('input', function() {
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        searchCategories(); // Llamada inicial sin especificar la página (por defecto, página 1)
    }, 50); // Ajusta el tiempo según tus necesidades
});

// Manejar la paginación
$(document).on('click', '.pagination__container-icon', function(e) {
    e.preventDefault(); // Evita que el enlace cargue la página completa
    var page = new URLSearchParams($(this).attr('href').split('?')[1]).get('page');
    searchCategories(page); // Realiza una búsqueda en la página seleccionada
});

