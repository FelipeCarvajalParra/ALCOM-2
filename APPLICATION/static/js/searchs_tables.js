function searchTable(module, page = 1, url) {
    let search; // Variable para almacenar la búsqueda

    switch(module) {
        case(1): // Caso para buscar referencias
            search = $('#searchReferences').val(); // Obtener el valor de búsqueda de referencias

            const filterBrandElement = document.getElementById('filterBrand');
            const filterBrandValue = filterBrandElement ? filterBrandElement.textContent.trim() : null;
            console.log(filterBrandValue)

            petition(url, search, page, filterBrandValue)
                .then(() => {
                    delete_confirmations();
                })
                .catch(() => {
                    console.log('error');
                });
            break;

        case(2): // Caso para buscar categorías
            search = $('#searchCategories').val(); // Obtener el valor de búsqueda de categorías

            petition(url, search, page)
                .then(() => {
                    modal_category();
                    delete_confirmations();
                    modal();
                })
                .catch(() => {
                    console.log('error');
                });
            break;

        default:
            search = ''; // Por si acaso
    }
}

function petition(url, search, page, brand) {
    return $.ajax({
        url: url,
        data: {
            'search': search,
            'page': page,
            'brand': brand
        }
    }).then(data => {
        $('.table__body').html(data.body);
        $('.table__footer').html(data.footer);
    });
}













let timeout;





paginatorReferences =  document.getElementById('paginatorReferences')

if(paginatorReferences){

    console.log('hola')

    $(document).on('input', '#searchReferences', function() {// Sección búsqueda categorías
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            searchTable(1, 1, '/view_categories/view_references/85'); // Llama a searchTable para categorías (página 1 por defecto)
        }, 350); // Tiempo de espera para debouncing
    });






    $(document).on('click', '.paginatorReferences', function(e) {
        e.preventDefault(); // Evita que el enlace cargue la página completa
        const page = new URLSearchParams($(this).attr('href').split('?')[1]).get('page');
        searchTable(1, page, '/view_categories/view_references/85'); // Realiza una búsqueda en la página seleccionada
    });
    
    // Observar cambios en el contenido del div filterBrand
    

    const filterBrand = document.getElementById('filterBrand');
    if (filterBrand) {
        const observer = new MutationObserver(function(mutationsList) {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList' || mutation.type === 'subtree') {
                    console.log('hola')
                    searchTable(1, 1, '/view_categories/view_references/85'); // Realiza la búsqueda al detectar cambios en filterBrand
                }
            }
        });
    
        observer.observe(filterBrand, { childList: true, subtree: true });
    }
}











paginatorCategories =  document.getElementById('paginatorCategories')

if(paginatorCategories){
    $(document).on('input', '#searchCategories', function() {// Sección búsqueda categorías
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            searchTable(2, 1, '/view_categories/'); // Llama a searchTable para categorías (página 1 por defecto)
        }, 350); // Tiempo de espera para debouncing
    });
    
    // Manejar la paginación para categorías
    $(document).on('click', '.paginatorCategories', function(e) {
        e.preventDefault(); // Evita que el enlace cargue la página completa
        const page = new URLSearchParams($(this).attr('href').split('?')[1]).get('page');
        searchTable(2, page, '/view_categories/'); // Realiza una búsqueda en la página seleccionada
    });
}

