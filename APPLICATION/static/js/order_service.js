// Inicialización de tooltips para los botones flotantes
const optionsTooltips = document.querySelectorAll('.floating-button__link');
optionsTooltips.forEach(option => {
    tippy(option, {
        content: option.dataset.tooltip,  // Contenido del tooltip
        placement: 'left',                // Posición del tooltip
        animation: 'scale',               // Animación de escala
        theme: 'custom-tooltip',          // Tema
        offset: [0, 10],                  // Desplazamiento del tooltip
        duration: [0, 0],                 // [entrada, salida] en milisegundos
        arrow: true
    });
});

// Referencias a los elementos clave
const order = document.getElementById('orderService'); // Elemento donde se muestra la orden
const numOrder = document.querySelector('.orden__date-table__number').textContent; // Número de la orden

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
