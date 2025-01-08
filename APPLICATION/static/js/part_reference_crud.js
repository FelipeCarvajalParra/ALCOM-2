const partElement = document.getElementById('idPart');
const partId = partElement ? partElement.value : null;

const addPartReferenceForm = document.getElementById('addPartReferenceForm');
const messagePartReferenceError = document.getElementById('messagePartReferenceError');

addPartReferenceForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    messagePartReferenceError.textContent = '‎';

    // Crear un objeto FormData para recoger los datos del formulario
    const formData = new FormData(addPartReferenceForm);

    formData.append('partId', partId);

    // Hacer una solicitud POST al servidor
    fetch('/new_part_reference/', {
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
            messagePartReferenceError.textContent = data.error;
        } else if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        messagePartReferenceError.textContent = 'Ha ocurrido un error en la validación.';
    });
});