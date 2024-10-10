window.onload = function() {
    console.log('hola');

    // Primera condición: Si la URL es '/print_users/', añade el evento de click para abrir la página de impresión
    if (window.location.pathname === '/view_users/') {
        var printButton = document.getElementById('printTable');
        if (printButton) { // Verifica que el botón exista antes de agregar el evento
            printButton.addEventListener('click', function() {
                window.open('/print_users/', '_blank');
            });
        }
    }

    // Segunda condición: Si la URL es '/print_users/', ejecuta la función de imprimir y cerrar la ventana
    if (window.location.pathname === '/print_users/') {
        window.print();  // Abrir el diálogo de impresión automáticamente

        window.onafterprint = function() {
            window.close();  // Cerrar la ventana después de la impresión
        };
    }
};
