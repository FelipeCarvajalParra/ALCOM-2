// Obtener referencias a los elementos del formulario
const names = document.getElementById('names');
const lastName = document.getElementById('lastName');
const email = document.getElementById('email');
const jobName = document.getElementById('jobName');
const form = document.querySelector('.container__form');
const messageError = document.getElementById('personalMessageError');
const userId1 = form.dataset.id; // Obtener el ID del usuario desde el atributo data-id

// Escuchar el evento de envío del formulario
form.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario

    // Limpiar mensajes de error previos
    messageError.textContent = '';

    // Crear el objeto de datos del formulario
    const formData = {
        names: names.value.trim(),
        lastName: lastName.value.trim(),
        email: email.value.trim(),
        jobName: jobName.value.trim(),
    };

    // Hacer una solicitud POST al servidor
    fetch(`/update_personal_data/${userId1}`, { // Usar el ID del usuario en la URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json()) // Procesar la respuesta como JSON
    .then(data => {
        // Mostrar mensaje de error basado en la respuesta del servidor
        if (data.success === false) {
            // Si hay un error, mostrar en el span
            messageError.textContent = data.error.email || data.error || 'Error desconocido';
        } else if (data.success === true) {
            // Si la actualización fue exitosa, recargar la página
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageError.textContent = 'Ha ocurrido un error en la validación.';
    });
});
