
const elements = document.querySelectorAll('.link_none');

    
elements.forEach(element => {
    element.addEventListener('click', function (event) {
        event.preventDefault(); // Previene el comportamiento por defecto del enlace (si es un enlace)
        
        // Muestra una alerta de SweetAlert2
        Swal.fire({
            title: '¡Enlace roto!',
            text: 'El enlace que has intentado abrir ya no existe.',
            icon: 'error',
            confirmButtonText: 'Aceptar',
            confirmButtonColor: '#3085d6',
        });

    });
});