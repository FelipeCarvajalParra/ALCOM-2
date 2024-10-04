(function() {
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
            // Mostrar mensaje de error basado en la respuesta del servidor
            if (data.success === false) {
                messageError.textContent = data.error;
            } else if (data.success) {
                // Si la actualización fue exitosa, mostrar un mensaje y recargar la página
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageError.textContent = 'Ha ocurrido un error en la validación.';
        });
    });
})();
