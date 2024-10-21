const fileInput = document.getElementById('file-upload');

if (fileInput) {

    console.log('hoplasss')
    fileInput.addEventListener('change', function() {
        const app_name = this.getAttribute('data-app');
        const table = this.getAttribute('data-table');
        const field = this.getAttribute('data-field');
        const record_id = this.getAttribute('data-record');
        const imageFile = this.files[0]; // Obtener el archivo de imagen seleccionado
        
        if (imageFile) {
            updateImage(app_name, table, field, record_id, imageFile);
        }
    });
}

function updateImage(app_name, table, field, record_id, image) {
    const formData = new FormData(); // Crear un objeto FormData para enviar el archivo
    formData.append('app_name', app_name);
    formData.append('table', table);
    formData.append('field', field);
    formData.append('record_id', record_id);
    formData.append('image', image); // Agregar la imagen al FormData

    fetch('/update_image/', {
        method: 'POST',
        body: formData, // Usar FormData como cuerpo de la solicitud
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(() => {
        location.reload(); // Recargar la página después de la actualización
    })
    .catch(error => {
        console.error('Error:', error); // Manejo de errores
    });

    // Reiniciar el input de archivo para permitir la selección de la misma imagen
    this.value = ''; // Esto permite seleccionar la misma imagen de nuevo
}
