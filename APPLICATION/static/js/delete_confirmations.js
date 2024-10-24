function delete_confirmations(){
    const logoutLink = document.getElementById('logout');
    const deleteUser = document.getElementById('deleteUser');
    const deleteActivityLogs = document.querySelectorAll('.deleteActivityLog');
    const deleteCategory = document.querySelectorAll('.deleteCategory');
    const deleteReference = document.querySelectorAll('.deleteReference');
    const deleteReferenceImage = document.getElementById('deleteReferenceImage');
    const deleteEquipment = document.querySelectorAll('.deleteEquipment')
    
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
    
    if (deleteReference) {
        deleteReference.forEach(function (logElement) {
            logElement.addEventListener('click', function () {
                const idReference = logElement.getAttribute('data-reference-id'); 
                const categoryId = document.getElementById('categoryId').dataset.categoryId;
                showConfirmationModal(
                    '¿Estás seguro?',
                    'La referencia, y existencias asociadas se perderan de forma permanente.',
                    'Sí, eliminar',
                    'Cancelar',
                    idReference,  
                    4,
                    categoryId         
                );
            });
        });
    }
    
    if (deleteReferenceImage) {
            deleteReferenceImage.addEventListener('click', function () {
                showConfirmationModal(
                    '¿Estás seguro?',
                    'La imagen se perdera de forma permanente.',
                    'Sí, eliminar',
                    'Cancelar',
                    0,  
                    5,
                    0         
                );
            });
    }

    if (deleteEquipment) {
        deleteEquipment.forEach(function (equipment) {
            equipment.addEventListener('click', function () {
                const equipmentId = equipment.getAttribute('data-id'); 
                const referenceId = document.getElementById('reference').value; 
                showConfirmationModal(
                    '¿Estás seguro?',
                    'El equipo y todas las intervenciones asociadas se perderan de forma permanente.',
                    'Sí, eliminar',
                    'Cancelar',
                    equipmentId, 
                    6,
                    referenceId
                );
            });
        });
    }

    
        
           
            
}
    
    
    function showConfirmationModal(title, text, confirmButtonText, cancelButtonText, recordId, action, urlAutoGenerate) {
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
                        case(4):
                            const idReference = arguments[4];  // recibir el ID aquí
                            const idCategory2 = arguments[6];
                            deleteRequest('delete_reference', idReference, `view_categories/view_references/${idCategory2}`, true);
                            break;
                        case(5):
                            const fileInput = document.getElementById('equipmentFileImageInput');
                            const app_name = fileInput.getAttribute('data-app');
                            const table = fileInput.getAttribute('data-table');
                            const field = fileInput.getAttribute('data-field');
                            const record_id = fileInput.getAttribute('data-record');
                            deleteFile(app_name, table, field, record_id)
                            break
                        case(6):
                            const equipmentId = arguments[4];  // recibir el ID aquí
                            const referenceId = arguments[6];

                            console.log(equipmentId, referenceId)

                            deleteRequest('delete_equipment', equipmentId, `edit_reference/${referenceId}`, true);
                            break
    
                    }
                }
            }
        }); 
    }
    
    function deleteRequest(url, id, returnView, autogenerate) {
        fetch(`/${url}/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Asegúrate de incluir el token CSRF
            }
        })
        .then(response => {
            if (response.ok) {
                if(autogenerate){
                    console.log('aqui1')
                    window.location.href = `/${returnView}`; 
                }else if(returnView){
                    console.log('aqui2')
                    window.location.href = `/${returnView}/`; 
                }else{
                    location.reload(true)
                }
            }
        })
        .catch(error => {
            console.log('aqui3')
            console.error('Error:', error);
        });
    }
        
    function deleteFile(app_name, table, field, record_id) {
        const formData = new FormData(); 
        formData.append('app_name', app_name);
        formData.append('table', table);
        formData.append('field', field);
        formData.append('record_id', record_id);

        fetch('/delete_file/', {
            method: 'POST',
            body: formData, 
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(() => {
            location.reload(); 
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // Reiniciar el input de archivo para permitir la selección de la misma imagen
        this.value = ''; // Esto permite seleccionar la misma imagen de nuevo
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


document.addEventListener('DOMContentLoaded', function() {
    delete_confirmations();
});
