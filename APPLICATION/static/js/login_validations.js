const user = document.getElementById('user');
const password = document.getElementById('password');
const form = document.querySelector('.login__access');
const messageError = document.getElementById('messageError');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío normal del formulario

    messageError.textContent = '‎';  // Limpiar mensajes de error previos

    // Obtener los valores del formulario
    const username = user.value.trim();
    const userPassword = password.value.trim();

    // Enviar la solicitud AJAX al servidor
    fetch('/login_validate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'username': username,
            'password': userPassword,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Mostrar mensaje de error recibido desde la vista
            messageError.textContent = data.error;
        } else if (data.success) {
            // Redirigir al usuario si el inicio de sesión es exitoso
            window.location.href = data.redirect_url;
        }
    })
    .catch(error => {
        messageError.textContent = 'Error en la validacion';
    });
});
