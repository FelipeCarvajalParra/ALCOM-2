const newPartForm = document.getElementById('newPartForm');
const messageNewPartError = document.getElementById('messageNewPartError');

const formData = new FormData(newPartForm);

console.log(formData)

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
    .then(response => response.json()) // Procesar la respuesta como JSON
    .then(data => {
        if (data.error) {
            messageNewPartError.textContent = data.error;
        } else if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageNewPartError.textContent = 'Ha ocurrido un error en la validación.';
    });
});
