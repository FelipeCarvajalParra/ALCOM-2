// Referencias a los elementos clave
const order = document.getElementById('orderService'); // Elemento donde se muestra la orden
const numOrder = document.querySelector('.orden__date-table__number').textContent; // Número de la orden
let selectedFile = null; // Variable para almacenar el archivo seleccionado
const { jsPDF } = window.jspdf;  // Accede al espacio global de jsPDF


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
            // Usar el archivo seleccionado o generar un PDF si no hay archivo
            const file = selectedFile || generatePDF(); // Si no hay archivo, genera el PDF
            saveIntervention('passed', file);
        }
    });
});

// Función para obtener el token CSRF
function getCSRFToken() {
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : null;
}

function generatePDF() {
    return new Promise((resolve, reject) => {
        html2canvas(order).then(canvas => {
            const pdf = new jsPDF({
                orientation: 'portrait', // Establecer orientación vertical
                unit: 'mm', // Unidades en milímetros
                format: 'a4', // Tamaño de la página A4
            });

            // Obtiene las dimensiones del canvas
            const imgWidth = 210; // A4 width en mm
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            // Si la imagen generada es más alta que la altura de la página A4 (297 mm), ajustamos el tamaño.
            if (imgHeight > 297) {
                const scaleFactor = 297 / imgHeight; // Escala proporcional
                canvas = document.createElement('canvas');
                canvas.width = canvas.width * scaleFactor;
                canvas.height = canvas.height * scaleFactor;
            }

            // Convierte el canvas a imagen JPEG
            const imgData = canvas.toDataURL('image/jpeg');

            // Agrega la imagen al PDF
            pdf.addImage(imgData, 'JPEG', 0, 0, imgWidth, imgHeight);

            // Guardar el PDF como Blob
            const pdfBlob = pdf.output('blob');
            const pdfFile = new File([pdfBlob], `${numOrder}.pdf`, { type: 'application/pdf' });

            // Verificar que pdfFile se genera correctamente antes de enviarlo
            if (pdfFile.size > 0) {
                resolve(pdfFile);
            } else {
                reject('Error: El archivo PDF no se generó correctamente');
            }
        }).catch(err => reject(err));
    });
}

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
            // Usar el archivo seleccionado o generar un PDF si no hay archivo
            const file = selectedFile || generatePDF(); // Si no hay archivo, genera el PDF

            // Verifica si `file` es una promesa
            if (file instanceof Promise) {
                file.then(pdfFile => {
                    saveIntervention('passed', pdfFile); // Llama a la función con el archivo generado
                }).catch(error => {
                    console.error(error);
                    Swal.fire({
                        title: 'Error',
                        text: 'No se pudo generar el PDF.',
                        icon: 'error'
                    });
                });
            } else {
                // Si no es una promesa, pásalo directamente
                saveIntervention('passed', file);
            }
        }
    });
});

function saveIntervention(result, file) {
    const formData = new FormData();
    formData.append('result', result);
    formData.append('numOrder', numOrder);

    console.log('Archivo enviado:', file);

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
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url; // Redirige al usuario
        } else if (data.message) {
            Swal.fire({
                title: 'Éxito',
                text: data.message,
                icon: 'success'
            }).then(() => {
                window.location.reload();
            });
        } else if (data.error) {
            Swal.fire({
                title: 'Error',
                text: data.error,
                icon: 'error'
            });
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        Swal.fire({
            title: 'Error',
            text: 'No se pudo conectar con el servidor.',
            icon: 'error'
        });
    });
}
