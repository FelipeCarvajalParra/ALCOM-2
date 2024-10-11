// Escuchar los clics en elementos por ID
const logoutLink = document.getElementById('logout');
const deleteUser = document.getElementById('deleteUser');
const deleteActivityLogs = document.querySelectorAll('.deleteActivityLog');
const deleteCategory = document.querySelectorAll('.deleteCategory');

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
            userId, // Pasa solo el ID de usuario aquí
            1
        );
    });
}

// Iterar sobre todos los elementos con clase 'deleteActivityLog'
if (deleteActivityLogs) {
    deleteActivityLogs.forEach(function (logElement) {
        logElement.addEventListener('click', function () {
            const idLog = logElement.getAttribute('data-idLog'); 
            console.log(idLog)
            showConfirmationModal(
                '¿Estás seguro?',
                'El registro se eliminará de forma permanente.',
                'Sí, eliminar',
                'Cancelar',
                idLog, // Pasa el ID del log aquí
                2
            );
        });
    });
}

if (deleteCategory) {
    deleteCategory.forEach(function (logElement) {
        logElement.addEventListener('click', function () {
            const idCategory = logElement.getAttribute('data-category-id'); 
            console.log(idCategory);
            // Asegúrate de que el ID se pasa correctamente
            showConfirmationModal(
                '¿Estás seguro?',
                'La categoria, equipos e intervenciones asociadas se perderan de forma permanente.',
                'Sí, eliminar',
                'Cancelar',
                idCategory,  // Pasa el ID del log aquí
                3           // El código para la eliminación
            );
        });
    });
}


function showConfirmationModal(title, text, confirmButtonText, cancelButtonText, recordId, action) {
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
            if (typeof recordId === 'string' && recordId.startsWith('/')) {
                // Redirigir a la URL especificada (por ejemplo, para cerrar sesión)
                window.location.href = recordId;
            } else {
                switch(action){
                    case(1):
                        deleteRequest('delete_user', recordId, 'view_users')
                        break;
                    case(2):
                        deleteRequest('delete_log_activity', recordId)
                        break;
                    case(3):
                        const idCategory = arguments[4];  // recibir el ID aquí
                        deleteRequest('delete_category', idCategory, 'view_categories');
                        break;
                }
            }
        }
    }); 
}

function deleteRequest(url, id, returnView) {
    console.log(id)
    fetch(`/${url}/${id}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Asegúrate de incluir el token CSRF
        }
    })
    .then(response => {
        if (response.ok) {
            if(returnView){
                window.location.href = `/${returnView}/`; 
            }else{
                location.reload(true)
            }
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



   