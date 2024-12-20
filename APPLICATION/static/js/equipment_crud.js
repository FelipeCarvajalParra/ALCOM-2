const newEquipmentForm = document.getElementById('newEquipmentForm');
const messageNewEquipmentError = document.getElementById('messageError');
const editEquipmentStateForm = document.getElementById('editEquipmentStateForm');
const messageEditEquipmentStateError = document.getElementById('messageEditEquipmentStateError');
const codeEquipment = document.getElementById('codeEquipment').textContent;

if (newEquipmentForm) {
    newEquipmentForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario
        messageNewEquipmentError.textContent = '‎';
    
        // Crear un objeto FormData para recoger los datos del formulario
        const formData = new FormData(newEquipmentForm);
    
        const selectedState = document.getElementById('equipmentState').textContent;
        formData.append('state', selectedState);
    
        // Hacer una solicitud POST al servidor
        fetch('/new_equipment/', {
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
                messageNewEquipmentError.textContent = data.error;
            } else if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            messageNewEquipmentError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}

if (editEquipmentStateForm) {
    editEquipmentStateForm.addEventListener('submit', function(event) {
        console.log('entra');

        event.preventDefault(); // Evitar el envío del formulario
        messageEditEquipmentStateError.textContent = '‎';

        // Obtener el valor de state
        const state = document.getElementById('equipmentState').textContent;

        // Crear un objeto FormData y añadir el valor de state
        const formData = new FormData(editEquipmentStateForm); // Incluye los campos del formulario
        formData.append('state', state);
        formData.append('codeEquipment', codeEquipment);

        // Hacer una solicitud POST al servidor
        fetch('/edit_equipment_state/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData // Enviar los datos del formulario con state incluido
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
                messageEditEquipmentStateError.textContent = data.error;
            } else if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            messageEditEquipmentStateError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}
