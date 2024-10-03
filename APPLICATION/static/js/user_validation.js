// Obtener referencias a los elementos del formulario
const names = document.getElementById('names');
const lastName = document.getElementById('lastName');
const email = document.getElementById('email');
const jobName = document.getElementById('jobName');
const username = document.getElementById('Usuario');
const newPassword = document.getElementById('newPassword');
const newPasswordValidation = document.getElementById('newPasswordValidation');
const statusSelect = document.querySelectorAll('.select--state')[0].querySelector('.select__selected');
const groupSelect = document.querySelectorAll('.select--state')[1].querySelector('.select__selected');
const form = document.querySelector('.container__form');
const messageError = document.getElementById('messageError');

// Escuchar el evento de envío del formulario
form.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario

    // Limpiar mensajes de error previos
    messageError.textContent = '‎';

    // Crear el objeto de datos del formulario
    const formData = {
        names: names.value.trim(),
        lastName: lastName.value.trim(),
        email: email.value.trim(),
        jobName: jobName.value.trim(),
        username: username.value.trim(),
        status: statusSelect.textContent.trim(),
        group: groupSelect.textContent.trim(),
        password: newPassword.value.trim(),
        password_validation: newPasswordValidation.value.trim(),
    };

    // Hacer una solicitud POST al servidor
    fetch('/register_user/', {
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
        if (data.error) {
            messageError.textContent = data.error;
        } else if (data.success) {
            // Recargar la página si el registro fue exitoso
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageError.textContent = 'Ha ocurrido un error en la validación.';
    });
});
