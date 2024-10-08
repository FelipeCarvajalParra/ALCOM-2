window.onload = function() {
    window.print();  // Abrir el diálogo de impresión automáticamente
    
    window.onafterprint = function() {
        window.close();  // Cerrar la ventana después de la impresión
    };
};