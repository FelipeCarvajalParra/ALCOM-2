function searchReferences(page = 1) {
    var search = $('#searchReferences').val();
    const categoryId = document.getElementById('categoryId').dataset.categoryId;
    const brand = filterBrand ? filterBrand.textContent.trim() : '';

    $.ajax({
        url: `/view_categories/view_references/${categoryId}`,
        data: {
            'search': search,
            'brand': brand,
            'page': page // Enviar la página actual también
        },
        success: function(data) {
            // Actualizar el cuerpo de la tabla
            $('.table__body').html(data.body);
            // Actualizar el pie de la tabla si lo proporciona el servidor
            $('.table__footer').html(data.footer); 
        }
    });
}

// Manejar la búsqueda con debounce
let timeout;

$('#searchReferences').on('input', function() {
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        searchReferences(); // Llamada inicial sin especificar la página (por defecto, página 1)
    }, 150); 
});

// Manejar la paginación
$(document).on('click', '.pagination__container-icon', function(e) {
    e.preventDefault(); // Evita que el enlace cargue la página completa
    var page = new URLSearchParams($(this).attr('href').split('?')[1]).get('page');
    searchReferences(page); // Realiza una búsqueda en la página seleccionada
});

// Observar cambios en el contenido del div filterBrand
const filterBrand = document.getElementById('filterBrand');

if (filterBrand) {
    const observer = new MutationObserver(function(mutationsList) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'subtree') {
                searchReferences(); // Realiza la búsqueda al detectar cambios en filterBrand
            }
        }
    });

    observer.observe(filterBrand, { childList: true, subtree: true });
}
