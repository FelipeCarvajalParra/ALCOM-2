
function searchReferences(page = 1) {
    console.log('hola')
    var search = $('#searchReferences').val();
    const categoryId = document.getElementById('categoryId').dataset.categoryId;
    var brand = filterBrand ? filterBrand.textContent.trim() : '';

    if(brand === 'Marca'){
        brand = ''
    }

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

