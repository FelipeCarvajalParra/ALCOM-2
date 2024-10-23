const newEquipmentForm = document.getElementById('newEquipmentForm');
const messageNewEquipmentError = document.getElementById('messageError');

newEquipmentForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    messageError.textContent = '‎';

    // Crear un objeto FormData para recoger los datos del formulario
    const formData = new FormData(newEquipmentForm);

    // Recoger el valor del estado seleccionado manualmente
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
    .then(response => response.json()) // Procesar la respuesta como JSON
    .then(data => {
        if (data.error) {
            messageNewEquipmentError.textContent = data.error;
        } else if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageNewEquipmentError.textContent = 'Ha ocurrido un error en la validación.';
    });
});
