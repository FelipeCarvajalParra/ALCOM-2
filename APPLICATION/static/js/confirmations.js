// Escuchar los clics en elementos por ID
const logoutLink = document.getElementById('logout');
const deleteUser = document.getElementById('deleteUser');

if (logoutLink) {
    logoutLink.addEventListener('click', function () {
        showConfirmationModal(
            '¿Estás seguro?',
            'Estás a punto de cerrar sesión.',
            'Sí, cerrar sesión',
            'Cancelar',
            '/logout_user/' // URL de cierre de sesión
        );
    });
}

if (deleteUser) {
    deleteUser.addEventListener('click', function () {
        const userId = deleteUser.getAttribute('data-user');
        showConfirmationModal(
            '¿Estás seguro?',
            'Si eliminas este usuario, también se eliminará toda la información relacionada (intervenciones, actividad, etc.).',
            'Sí, eliminar',
            'Cancelar',
            userId // Pasa solo el ID de usuario aquí
        );
    });
}

function showConfirmationModal(title, text, confirmButtonText, cancelButtonText, userIdOrRedirectUrl) {
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
            if (typeof userIdOrRedirectUrl === 'string' && userIdOrRedirectUrl.startsWith('/')) {
                // Redirigir a la URL especificada (por ejemplo, para cerrar sesión)
                window.location.href = userIdOrRedirectUrl;
            } else {
                // Si es un ID de usuario, ejecutar la función de eliminación
                deleteUserRequest(userIdOrRedirectUrl); // Llama a la función para eliminar el usuario
            }
        }
    });
}

function deleteUserRequest(userId) {
    fetch(`/delete_user/${userId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Asegúrate de incluir el token CSRF
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/view_users/'; // Asigna la URL directamente
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Comprobar si este cookie comienza con el nombre que buscamos
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



   