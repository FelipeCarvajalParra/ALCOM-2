const referenceForm = document.getElementById('referenceForm'); // Asegúrate de que el ID coincida
const messageError = document.getElementById('referenceMessageError');
var categoryId = document.getElementById('categoryId')

if(categoryId){
    categoryId = document.getElementById('categoryId').dataset.categoryId;
}

if(referenceForm){
    referenceForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario
        messageError.textContent = '‎'; // Limpiar mensajes de error
    
        const formData = {
            reference: document.getElementById('newReference').value.trim(),
            brand: document.getElementById('brand').value.trim(),
            url: document.getElementById('url').value.trim(),
            accessories: document.getElementById('accessories').value.trim(),
            observations: document.getElementById('observations').value.trim(),
        };
    
        // Capturar los valores de los campos dinámicos
        const components = [];
        document.querySelectorAll('textarea[id]').forEach(textarea => {
            const campoId = textarea.id.replace('campo_', ''); // Extraer el ID del campo
            const value = textarea.value.trim();
            if (campoId !== 'accessories' && campoId !== 'observations') {
                components.push({ campoId: campoId, valor: value });
            }
        });
    
        formData.components = components; // Añadir los componentes al objeto de datos}
    
        // Hacer una solicitud POST al servidor
        fetch(`/new_reference/${categoryId}`, { // Cambia 'id_category' según sea necesario
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(formData) 
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
                messageError.textContent = data.error; // Mostrar error
            } else if (data.success) {
                // Recargar la página si la referencia fue creada con éxito
                location.reload();
            }
        })
        .catch(error => {
            messageError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });    
}

var idReference = document.getElementById('reference');
if(idReference){
    idReference = document.getElementById('reference').value;
}

const referenceEditForm = document.getElementById('referenceEditForm'); // Asegúrate de que el ID coincida
const messageEditError = document.getElementById('referenceEditMessageError');

if(referenceEditForm){
    referenceEditForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario
        messageEditError.textContent = '‎'; // Limpiar mensajes de error
    
        const formData = new FormData(referenceEditForm); // Crea un objeto FormData con los datos del formulario
    
        // Hacer una solicitud POST al servidor
        fetch(`/edit_reference_data_general/${idReference}`, { 
            method: 'POST',
            body: formData, // Envía los datos del formulario
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
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

const referenceEditComponentsForm = document.getElementById('referenceEditComponentsForm'); // Asegúrate de que el ID coincida
const messageEditComponentsError = document.getElementById('referenceEditComponentsMessageError');

if(referenceEditComponentsForm){
    referenceEditComponentsForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario
        messageEditComponentsError.textContent = '‎'; // Limpiar mensajes de error
    
        const formData = new FormData(referenceEditComponentsForm); // Crea un objeto FormData con los datos del formulario
    
        // Hacer una solicitud POST al servidor
        fetch(`/edit_reference_components/${idReference}`, { 
            method: 'POST',
            body: formData, // Envía los datos del formulario
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
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
                messageEditComponentsError.textContent = data.error; // Mostrar error
            } else {
                location.reload();
            }
        })
        .catch(error => {
            messageEditComponentsError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });

    
}







