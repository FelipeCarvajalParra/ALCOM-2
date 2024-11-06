function searchTable(module, page = 1, url) {
    let search; // Variable para almacenar la búsqueda

    switch(module) {
        case(1): // Caso para buscar referencias
            search = $('#searchReferences').val(); // Obtener el valor de búsqueda de referencias

            const filterBrandElement = document.getElementById('filterBrand');
            const filterBrandValue = filterBrandElement ? filterBrandElement.textContent.trim() : null;

            petition(url, search, page, filterBrandValue)
                .then(() => {
                    delete_confirmations();
                    tooltip()
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
                    tooltip()
                })
                .catch(() => {
                    console.log('error');
                });
            break;
        
        case(3): // Caso para buscar categorías
            search = $('#searchEquipment').val();

            petition(url, search, page)
                .then(() => {
                    delete_confirmations();
                    tooltip()
                })
                .catch(() => {
                    console.log('error');
                });
            break;
        case(4):
            search = $('#searchEquipment').val();

            const filterBrandEquipmentElement = document.getElementById('filterBrand');
            const filterBrandEquipmentValue = filterBrandEquipmentElement ? filterBrandEquipmentElement.textContent.trim() : null;

            const filterCategoryEquipmentElement = document.getElementById('filterCategory');
            const filterCategoryEquipmentValue = filterCategoryEquipmentElement ? filterCategoryEquipmentElement.textContent.trim() : null;
            

            petition(url, search, page, filterBrandEquipmentValue, filterCategoryEquipmentValue)
                .then(() => {
                    delete_confirmations();
                    tooltip()
                })
                .catch(() => {
                    console.log('error');
                });
            break;
        case(5): // Caso para buscar categorías
            search = $('#searchUser').val();

            petition(url, search, page)
                .then(() => {
                    tooltip()
                })
                .catch(() => {
                    console.log('error');
                });
            break;

        case (6):
            search = $('#searchPart').val();

            petition(url, search, page)
                .then(() => {
                    tooltip()
                })
                .catch(() => {
                    console.log('error');
                });
            break;

        default:
            search = ''; 
    }
}

function petition(url, search, page, brand, category) {
    // Crear el objeto de datos a enviar
    let data = {
        'search': search,
        'page': page,
        'brand': brand,
        'category': category
    };

    // Enviar la petición AJAX
    return $.ajax({
        url: url,
        data: data
    }).then(data => {
        $('.table__body').html(data.body);
        $('.table__footer').html(data.footer);
    });
}

let timeout;

paginatorReferences =  document.getElementById('paginatorReferences')
if(paginatorReferences){

    const category = document.getElementById('reference').value

    $(document).on('input', '#searchReferences', function() {// Sección búsqueda categorías
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            searchTable(1, 1, `/view_categories/view_references/${category}`); // Llama a searchTable para categorías (página 1 por defecto)
        }, 350); // Tiempo de espera para debouncing
    });

    const filterBrand = document.getElementById('filterBrand');
    if (filterBrand) {
        const observer = new MutationObserver(function(mutationsList) {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList' || mutation.type === 'subtree') {
                    searchTable(1, 1, `/view_categories/view_references/${category}`); // Realiza la búsqueda al detectar cambios en filterBrand
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
}

paginatorEquipment =  document.getElementById('paginatorEquipment')
if(paginatorEquipment){
    const reference = document.getElementById('reference').value
    $(document).on('input', '#searchEquipment', function() {// Sección búsqueda categorías
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            searchTable(3, 1, `/edit_reference/${reference}`); // Llama a searchTable para categorías (página 1 por defecto)
        }, 350); // Tiempo de espera para debouncing
    });
}

paginatorEquipment =  document.getElementById('paginatorEquipmentPage')
if(paginatorEquipment){

    $(document).on('input', '#searchEquipment', function() {// Sección búsqueda categorías
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            searchTable(4, 1, `/view_equipments/`); 
        }, 350); 
    });

    const filterBrand = document.getElementById('filterBrand');
    if (filterBrand) {
        const observer = new MutationObserver(function(mutationsList) {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList' || mutation.type === 'subtree') {
                    searchTable(4, 1, `/view_equipments/`); 
                }
            }
        });
    
        observer.observe(filterBrand, { childList: true, subtree: true });
    }

    const filterCategory = document.getElementById('filterCategory');
    if (filterCategory) {
        const observer = new MutationObserver(function(mutationsList) {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList' || mutation.type === 'subtree') {
                    searchTable(4, 1, `/view_equipments/`); 
                }
            }
        });
    
        observer.observe(filterCategory, { childList: true, subtree: true });
    }
}

paginatorUsers =  document.getElementById('paginatorUsers')
if(paginatorUsers){
    $(document).on('input', '#searchUser', function() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            searchTable(5, 1, `/view_users/`); // Llama a searchTable para categorías (página 1 por defecto)
        }, 350); // Tiempo de espera para debouncing
    });
}


paginatorParts =  document.getElementById('paginatorParts')
if(paginatorParts){
    $(document).on('input', '#searchPart', function() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            searchTable(6, 1, `/view_inventory_parts/`); // Llama a searchTable para categorías (página 1 por defecto)
        }, 350); // Tiempo de espera para debouncing
    });
}
