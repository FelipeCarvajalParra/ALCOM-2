// Escuchar los clics en elementos por ID
const logoutLink = document.getElementById('logout');
const deleteLink = document.getElementById('delete-item-1');

if (logoutLink) {
    logoutLink.addEventListener('click', function () {
        showConfirmationModal(
            '¿Estás seguro?',
            'Estás a punto de cerrar sesión.',
            'Sí, cerrar sesión',
            'Cancelar',
            '/logout_user/' // Reemplaza con la URL real para cerrar sesión
        );
    });
}

if (deleteLink) {
    deleteLink.addEventListener('click', function () {
        showConfirmationModal(
            'Confirmar eliminación',
            '¿Estás seguro de que deseas eliminar este elemento?',
            'Sí, eliminar',
            'Cancelar',
            'url_para_eliminar_item' // Reemplaza con la URL real para eliminar el item
        );
    });
}

function showConfirmationModal(title, text, confirmButtonText, cancelButtonText, redirectUrl) {
    Swal.fire({
        title: title,
        text: text,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: confirmButtonText,
        cancelButtonText: cancelButtonText
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = redirectUrl; // Redirigir a la URL especificada
        }
    });
}




   