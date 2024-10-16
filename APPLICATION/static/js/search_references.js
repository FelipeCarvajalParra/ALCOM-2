function searchReferences() {
    var search = $('#searchReferences').val();
    const categoryId = document.getElementById('categoryId').dataset.categoryId;
    const brand = filterBrand ? filterBrand.textContent.trim() : '';

    $.ajax({
        url: `/view_categories/view_references/${categoryId}`,
        data: {
            'search': search,
            'brand': brand  // Asegúrate de enviar el texto, no el nodo
        },
        success: function(data) {
            $('.table__body').html(data);
        }
    });
}

let timeout;

$('#searchReferences').on('input', function() {
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        searchReferences();
    }, 150); 
});

const filterBrand = document.getElementById('filterBrand');

if (filterBrand) {
    // Observar cambios en el contenido del div filterBrand
    const observer = new MutationObserver(function(mutationsList) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'subtree') {
                searchReferences();
            }
        }
    });

    // Configurar el observer para observar cambios en el contenido del div
    observer.observe(filterBrand, { childList: true, subtree: true });
}
