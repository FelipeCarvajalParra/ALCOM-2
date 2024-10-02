// Selecciona el input, el contenedor de búsqueda y la capa de color
const searchInput = document.querySelector('.main__search-input');
const searchContainer = document.querySelector('.container--search');
const layerColor = document.querySelector('.layer-color'); // Capa de color

// Muestra el contenedor solo si hay texto en el input
searchInput.addEventListener('input', function() {
    if (this.value.trim() === '') {
        searchContainer.style.display = 'none'; // Oculta si no hay texto
        layerColor.style.display = 'none'; // Oculta la capa de color
    } else {
        searchContainer.style.display = 'block'; // Muestra si hay texto
        layerColor.style.display = 'block'; // Muestra la capa de color
    }
});

// Oculta el contenedor de búsqueda cuando se pierde el foco
searchInput.addEventListener('blur', function() {
    // Usa un timeout para permitir el clic en el contenedor
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
    // Si el clic no es dentro del contenedor de búsqueda o del input
    if (!searchContainer.contains(event.target) && !searchInput.contains(event.target)) {
        searchContainer.style.display = 'none'; // Oculta el contenedor de búsqueda
        layerColor.style.display = 'none'; // Oculta la capa de color
    }
});
