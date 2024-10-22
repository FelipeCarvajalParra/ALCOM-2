const equipmentFileImageInput = document.getElementById('equipmentFileImageInput');
const equipmentFileSheetInput = document.getElementById('equipmentFileSheetInput'); 

if (equipmentFileImageInput) {
    equipmentFileImageInput.addEventListener('change', function() {
        const app_name = this.getAttribute('data-app');
        const table = this.getAttribute('data-table');
        const field = this.getAttribute('data-field');
        const record_id = this.getAttribute('data-record');
        const type = this.getAttribute('data-type');
        const file = this.files[0]; // Obtener el archivo de imagen seleccionado
        
        if (file) {
            updateFile(app_name, table, field, record_id, file, type);

        }
    });
}

if (equipmentFileSheetInput) {
    equipmentFileSheetInput.addEventListener('change', function() {
        const app_name = this.getAttribute('data-app');
        const table = this.getAttribute('data-table');
        const field = this.getAttribute('data-field');
        const record_id = this.getAttribute('data-record');
        const type = this.getAttribute('data-type');
        const file = this.files[0]; 
        
        if (file) {
            updateFile(app_name, table, field, record_id, file, type);
        }
    });
}

function updateFile(app_name, table, field, record_id, file, type) {
    const formData = new FormData(); // Crear un objeto FormData para enviar el archivo
    formData.append('app_name', app_name);
    formData.append('table', table);
    formData.append('field', field);
    formData.append('record_id', record_id);
    formData.append('type', type);
    formData.append('file', file); // Agregar la imagen al FormData

    fetch('/update_file/', {
        method: 'POST',
        body: formData, // Usar FormData como cuerpo de la solicitud
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(() => {
        location.reload(); // Recargar la página después de la actualización
    })

    // Reiniciar el input de archivo para permitir la selección de la misma imagen
    this.value = ''; // Esto permite seleccionar la misma imagen de nuevo
}
