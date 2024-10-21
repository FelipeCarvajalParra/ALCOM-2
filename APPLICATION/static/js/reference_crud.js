const referenceForm = document.getElementById('referenceForm'); // Asegúrate de que el ID coincida
const messageError = document.getElementById('referenceMessageError');
const categoryId = document.getElementById('categoryId').dataset.categoryId;

console.log(categoryId)

referenceForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    messageError.textContent = '‎'; // Limpiar mensajes de error

    const formData = {
        reference: document.getElementById('reference').value.trim(),
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
        if (value) {
            if (campoId !== 'accessories' && campoId !== 'observations') {
                console.log(campoId);
                components.push({ campoId: campoId, valor: value });
            }
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
    .then(response => response.json()) // Procesar la respuesta como JSON
    .then(data => {
        if (data.error) {
            messageError.textContent = data.error; // Mostrar error
        } else if (data.success) {
            // Recargar la página si la referencia fue creada con éxito
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageError.textContent = 'Ha ocurrido un error en la validación.';
    });
});
