downloadFileEquipment = document.getElementById('downloadFileEquipment');


downloadFileEquipment.addEventListener('click', function(){

    const fileDownload = document.getElementById('equipmentFileImageInput');

    const app_name = fileDownload.getAttribute('data-app');
    const table = fileDownload.getAttribute('data-table');
    const field = fileDownload.getAttribute('data-field');
    const record_id = fileDownload.getAttribute('data-record');
    
    download_file(app_name, table, field, record_id)
})


function download_file(app_name, table, field, record_id) {
    const formData = new FormData(); 
    formData.append('app_name', app_name);
    formData.append('table', table);
    formData.append('field', field);
    formData.append('record_id', record_id);

    fetch('/download_file/', {
        method: 'POST',
        body: formData, 
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => {
        if (response.ok) {
            const disposition = response.headers.get('Content-Disposition');
            let fileName = 'downloaded_file';
            if (disposition && disposition.includes('filename=')) {
                const matches = disposition.match(/filename="?([^"]+)"?/);
                if (matches && matches[1]) {
                    fileName = matches[1];
                }
            }
            return response.blob().then(blob => ({ blob, fileName }));
        }
    })
    .then(({ blob, fileName }) => {
        if (blob) {
            // Crear un enlace para descargar el archivo con el nombre adecuado
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = fileName; // Nombre del archivo desde el servidor
            document.body.appendChild(a);
            a.click(); // Iniciar la descarga
            window.URL.revokeObjectURL(url); // Liberar el objeto URL
        }
    })
    .finally(() => {
        location.reload(); // Siempre recargar la página al final, independientemente del resultado
    });
}

