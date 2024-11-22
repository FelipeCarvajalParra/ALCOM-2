function addEventListenersToSelectElement(selectElement) {
    const selectedElement = selectElement.querySelector('.select__selected');
    const optionsElement = selectElement.querySelector('.select__options');

    // Verificar si los elementos existen antes de añadir los event listeners
    if (selectedElement && optionsElement) {
        // Al hacer clic en cualquier parte del select, mostrar/ocultar las opciones
        selectElement.addEventListener('click', function(e) {
            // Evita que el evento se propague al hacer clic en las opciones
            if (e.target.classList.contains('select__option')) return;
            selectElement.classList.toggle('select--active');
        });

        // Al hacer clic en una opción, cambiar el texto seleccionado y ocultar las opciones
        optionsElement.addEventListener('click', function(e) {
            if (e.target.classList.contains('select__option')) {
                // Si es una opción de export, cerrar el menú
                if (e.target.classList.contains('select__option--export')) {
                    selectElement.classList.remove('select--active'); // Cierra el menú
                } else {
                    selectedElement.textContent = e.target.textContent;
                    selectElement.classList.remove('select--active'); // Cierra el menú
                }
            }
        });

        // Cerrar el desplegable si se hace clic fuera
        document.addEventListener('click', function(e) {
            if (!selectElement.contains(e.target)) {
                selectElement.classList.remove('select--active');
            }
        });
    }
}

function filterSelector() {
    const selectElements = document.querySelectorAll('.select--filter');
    selectElements.forEach(selectElement => {
        addEventListenersToSelectElement(selectElement);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    filterSelector();
});