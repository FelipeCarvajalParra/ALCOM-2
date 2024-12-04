const createUser = document.getElementById('modalNewUser')
if(createUser){
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
            messageError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}    

const updateUser = document.getElementById('personalDataContainer')
if(updateUser){
    const names = document.getElementById('names');
    const lastName = document.getElementById('lastName');
    const email = document.getElementById('email');
    const jobName = document.getElementById('jobName');
    const form = document.querySelector('.container__form');
    const messageError = document.getElementById('personalMessageError');
    const userId1 = form.dataset.id; 

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
            messageError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}

const updateLoginUser = document.getElementById('personalDataContainer')
if(updateLoginUser){
    const loginForm = document.getElementById('loginDataForm');
    const userId = loginForm.getAttribute('data-id');
    const usernameInput = document.getElementById('username');
    const newPasswordInput = document.getElementById('newPassword');
    const newPasswordValidationInput = document.getElementById('newPasswordValidation');
    const statusSelect = document.querySelectorAll('.select--state')[0].querySelector('.select__selected');
    const roleSelect = document.querySelectorAll('.select--state')[1].querySelector('.select__selected');
    const messageError = document.getElementById('loginMessageError');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario

        // Limpiar mensajes de error previos
        messageError.textContent = '';

        // Crear el objeto de datos del formulario
        const formData = {
            username: usernameInput.value.trim(),
            status: statusSelect.textContent.trim(),
            role: roleSelect.textContent.trim(),
            password: newPasswordInput.value.trim(),
            password_validation: newPasswordValidationInput.value.trim(),
        };

        // Hacer una solicitud POST al servidor
        fetch(`/update_login_data/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === false) {
                messageError.textContent = data.error;
            } else if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            messageError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
}