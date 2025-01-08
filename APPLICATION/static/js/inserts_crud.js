const addPartForm = document.getElementById('addPartForm');
const messageAddError = document.getElementById('messageAddError');
const idPartAdd = document.getElementById('idPart').value

if(addPartForm){
    addPartForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario
        messageAddError.textContent = '';
    
        // Obtener el valor seleccionado de la acción
        const actionSelected = document.querySelector('.select__selected--action').textContent.trim();
    
        // Crear un objeto FormData para recoger los datos del formulario
        const formData = new FormData(addPartForm);
    
        // Añadir el valor de la acción seleccionada al objeto FormData
        formData.set('action', actionSelected);
    
        // Enviar la solicitud con fetch
        fetch(`/add_parts/${idPartAdd}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData // Enviar los datos del formulario
        })
        .then(response => {
            if (response.status === 403) {
                window.location.href = '/forbidden_access/';  
                return; // Salir de la promesa
            }
    
            return response.json();
        }) 
        .then(data => {
            if (data.error) {
                messageAddError.textContent = data.error;
            } else if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            messageAddError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}



