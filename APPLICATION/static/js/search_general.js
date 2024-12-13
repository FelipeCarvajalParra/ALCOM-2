const searchInput = document.getElementById('inputSearchGeneral');
const searchContainer = document.getElementById('containerSearch');
const layerColor = document.querySelector('.layer-color'); 

// Muestra el contenedor solo si hay texto en el input
searchInput.addEventListener('input', function() {
    if (this.value.trim() === '') {
        searchContainer.style.display = 'none';
        layerColor.style.display = 'none';
    } else {
        searchContainer.style.display = 'block'; // Muestra si hay texto
        layerColor.style.display = 'block'; // Muestra la capa de color
    }
});

// Oculta el contenedor de búsqueda cuando se pierde el foco
searchInput.addEventListener('blur', function() {
    setTimeout(() => {
        if (this.value.trim() === '') {
            searchContainer.style.display = 'none'; // Oculta si no hay texto
            layerColor.style.display = 'none'; // Oculta la capa de color
        }
    }, 200);
});

// Evita que el contenedor se oculte cuando se hace clic dentro de él
searchContainer.addEventListener('mousedown', function(event) {
    event.stopPropagation(); // Previene el evento de blur en el input
});

// Cierra el contenedor de búsqueda si se hace clic fuera del contenedor o del input
document.addEventListener('click', function(event) {
    if (!searchContainer.contains(event.target) && !searchInput.contains(event.target)) {
        searchContainer.style.display = 'none'; // Oculta el contenedor de búsqueda
        layerColor.style.display = 'none'; // Oculta la capa de color
    }
});

let timeoutGeneral;

function petitionSearchGeneral(url, search) {
    let data = {
        'search_general': search,
    };

    return $.ajax({
        url: url,
        data: data,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        method: 'GET'  
    }).then(response => {
        $('.container--search-general').html(response.body);
    });
}

$(document).on('input', '#inputSearchGeneral', function() {
    clearTimeout(timeoutGeneral);
    const inputSearchGeneral = $('#inputSearchGeneral').val().trim();

    // Evita la petición si el campo está vacío
    if (!inputSearchGeneral) {
        $('.container--search').html('<div class="search-section"><div class="search-section__title search-section__title--result-none">Sin resultados</div></div>');
        return;
    }

    // Muestra el spinner o mensaje de carga
    $('.container--search').html('<div class="search-section"><div class="search-section__loading">Cargando...</div></div>');

    timeout = setTimeout(function() {
        petitionSearchGeneral('/search_general/', inputSearchGeneral);
    }, 350);
});