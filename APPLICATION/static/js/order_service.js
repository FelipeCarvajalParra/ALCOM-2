// Referencias a los elementos clave
const order = document.getElementById('orderService'); // Elemento donde se muestra la orden
const numOrder = document.querySelector('.orden__date-table__number').textContent; // Número de la orden
let selectedFile = null; // Variable para almacenar el archivo seleccionado

// Listener para descargar PNG
document.getElementById('downloadPNG').addEventListener('click', () => {
    html2canvas(order).then(canvas => {
        const link = document.createElement('a');
        link.download = `${numOrder}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
});

// Listener para imprimir PDF
document.getElementById('downloadPDF').addEventListener('click', () => {
    const embedElement = document.querySelector('.orden--embed');
    if (embedElement) {
        // Manejar PDFs cargados externamente
        const fileURL = embedElement.getAttribute('src');
        const newWindow = window.open(fileURL, '_blank');
        if (newWindow) {
            newWindow.focus();
        } else {
            alert('Permite ventanas emergentes para imprimir este archivo.');
        }
    } else {
        // Imprime el contenido original de la orden
        const originalContent = document.body.innerHTML; // Guarda el contenido original de la página
        document.body.innerHTML = order.outerHTML;
        window.print();
        document.body.innerHTML = originalContent;
        window.location.reload(); // Recarga para restablecer los eventos y estilos
    }
});

// Botón flotante para activar el selector de archivos
document.getElementById('uploadFileButton').addEventListener('click', () => {
    document.getElementById('uploadFile').click(); // Dispara el input oculto
});

// Listener para manejar el archivo seleccionado
document.getElementById('uploadFile').addEventListener('change', (event) => {
    const file = event.target.files[0]; // Obtiene el archivo seleccionado
    selectedFile = file; // Guarda el archivo en la variable global

    if (file && file.type === 'application/pdf') {
        const fileURL = URL.createObjectURL(file); // Crea un enlace temporal al archivo

        // Reemplaza el contenido de la orden con un visor PDF
        order.innerHTML = `
            <embed class="orden--embed" src="${fileURL}" type="application/pdf" width="100%" height="600px" />
        `;

        // Oculta o elimina los botones de descarga
        document.getElementById('downloadPNG').style.display = 'none'; // Oculta el botón PNG
        document.getElementById('downloadPDF').style.display = 'none'; // Oculta el botón PDF

    } else {
        alert('Por favor, selecciona un archivo PDF válido.');
    }
});

// Rechazar intervención
document.getElementById('orderDenied').addEventListener('click', () => {
    Swal.fire({
        title: '¿Estás seguro?',
        text: 'La intervención y todos sus movimientos se perderán de forma permanente.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            saveIntervention('denied', null);
        }
    });
});

// Aprobar intervención
document.getElementById('orderPassed').addEventListener('click', () => {
    Swal.fire({
        title: '¿Estás seguro?',
        text: 'Una vez aprobada la intervención no podrá ser modificada.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, aprobar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const file = selectedFile || generatePDF(); // Usar archivo cargado o generar el PDF
            saveIntervention('passed', file);
        }
    });
});

// Generar PDF del contenido de la orden
function generatePDF() {
    const canvas = document.createElement('canvas');
    html2canvas(order).then(canvas => {
        canvas.toBlob(blob => {
            const pdfFile = new File([blob], `${numOrder}.pdf`, { type: 'application/pdf' });
            saveIntervention('passed', pdfFile);
        });
    });
}

function getCSRFToken() {
    // Busca el token CSRF desde las cookies
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : null;
}

function saveIntervention(result, file) {
    const formData = new FormData();
    formData.append('result', result);
    formData.append('numOrder', numOrder);

    if (file) {
        formData.append('file', file); // Adjunta el archivo si existe
    }

    fetch(`/save_result_intervention/${numOrder}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken() // Agrega el token CSRF al encabezado
        },
        body: formData // Envía FormData para manejar datos y archivos
    })
    .then(response => {
        if (response.ok) {
            // Si el servidor responde correctamente, recarga la página
            Swal.fire({
                title: 'Éxito',
                text: 'La intervención se ha guardado correctamente.',
                icon: 'success'
            }).then(() => {
                window.location.reload();
            });
        } else {
            Swal.fire({
                title: 'Error',
                text: 'Hubo un problema al guardar la intervención.',
                icon: 'error'
            });
        }
    })
    .catch(error => {
        // Manejar errores de red u otros problemas
        console.error('Error en la solicitud:', error);
        Swal.fire({
            title: 'Error',
            text: 'No se pudo conectar con el servidor.',
            icon: 'error'
        });
    });
}
