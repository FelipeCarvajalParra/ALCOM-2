document.getElementById('imageProfile').addEventListener('click', function() {
    document.getElementById('image').click();
});

document.getElementById('image').addEventListener('change', function() {
    // Verifica si se ha seleccionado un archivo
    if (this.files && this.files[0]) {
        // Crear FormData y llenar con datos
        const formData = new FormData();
        formData.append('app_name', document.getElementById('app_name').value);
        formData.append('table', document.getElementById('table').value);
        formData.append('field', document.getElementById('field').value);
        formData.append('userId', document.getElementById('userId').value);
        formData.append('image', this.files[0]);  // Agregar la imagen seleccionada

        // Enviar el formulario como una solicitud POST
        fetch('/update_image/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(() => {
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // Reiniciar el input de archivo para permitir la selección de la misma imagen
        this.value = '';  // Esto permite seleccionar la misma imagen de nuevo
    }
});