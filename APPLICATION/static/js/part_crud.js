const newPartForm = document.getElementById('newPartForm');
const messageNewPartError = document.getElementById('messageNewPartError');

if(newPartForm){
    newPartForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario
        messageNewPartError.textContent = '‎';
    
        // Crear un objeto FormData para recoger los datos del formulario
        const formData = new FormData(newPartForm);
    
        fetch('/new_part/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData // Enviar los datos del formulario
        })
        .then(response => {
            if (response.status === 403) {
                window.location.href = '/forbidden_access/';  
                return; 
            }
            return response.json();
        }) 
        .then(data => {
            if (data.error) {
                messageNewPartError.textContent = data.error;
            } else if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            messageNewPartError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}


const partEditForm = document.getElementById('partEditForm'); // Asegúrate de que el ID coincida
const messageEditError = document.getElementById('partEditMessageError');

if(partEditForm){
    const idPart = document.getElementById('idPart').value
    partEditForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario
        messageEditError.textContent = '‎'; // Limpiar mensajes de error
    
        const formData = new FormData(partEditForm); // Crea un objeto FormData con los datos del formulario
    
        // Hacer una solicitud POST al servidor
        fetch(`/edit_part_action/${idPart}`, { 
            method: 'POST',
            body: formData, // Envía los datos del formulario
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
        })
        .then(response => response.json()) // Asegúrate de procesar la respuesta como JSON
        .then(data => {
            if (data.error) {
                messageEditError.textContent = data.error; // Mostrar error
            } else {
                location.reload();
            }
        })
        .catch(error => {
            messageEditError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}
