function petitionSearchTables(url, page, search, brand, category) {
    let data = {
        'search': search,
        'brand': brand,
        'category':category,
        'page': page,
    };

    return $.ajax({
        url: url,
        data: data,
        method: 'GET',
    }).then(response => {
        $('.container__references').html(response.body);
        $('.table__footer').html(response.footer);
    });
}

// Referencias a los elementos
const filterBrandElement = document.getElementById('filterBrand');
const filterCategoryElement = document.getElementById('filterCategory');
const inputSearchReferencesElement = document.getElementById('inputSearchReferences');

function executePetition() {
    // Obtener los valores actuales de los tres filtros
    const inputSearchValue = inputSearchReferencesElement ? inputSearchReferencesElement.value.trim() : '';
    const filterBrandValue = filterBrandElement ? filterBrandElement.textContent.trim() : '';
    const filterCategoryValue = filterCategoryElement ? filterCategoryElement.textContent.trim() : '';
    
    // Llamada a la función petition con los valores de los tres elementos
    petitionSearchTables('/view_all_references/', 1, inputSearchValue, filterBrandValue, filterCategoryValue);
}

// Evento para `inputSearchReferences` que detecta cambios de input
let timeoutReferences;
$(document).on('input', '#inputSearchReferences', function() {
    clearTimeout(timeoutReferences);
    timeoutReferences = setTimeout(executePetition, 350);
});

// Configuración de MutationObserver para `filterBrand` y `filterCategory`
if (filterBrandElement || filterCategoryElement) {
    const observer = new MutationObserver(function(mutationsList) {
        // Ejecuta la petición al detectar cambios en cualquiera de los elementos observados
        executePetition();
    });

    // Observar ambos elementos con el mismo observador
    if (filterBrandElement) {
        observer.observe(filterBrandElement, { childList: true, subtree: true });
    }
    if (filterCategoryElement) {
        observer.observe(filterCategoryElement, { childList: true, subtree: true });
    }
}

