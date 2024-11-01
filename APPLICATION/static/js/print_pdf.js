const printUsersPdf = document.getElementById('printUsersPdf');

if (printUsersPdf) {
    printUsersPdf.addEventListener('click', function () {
        const app_name = 'users'
        const table = 'customUser'
        const fields_table = [ 'first_name', 'last_name', 'username', 'email', 'position']
        const fields_pdf = [ 'Nombres', 'Apellidos', 'Usurio', 'Correo', 'Cargo']
        printPdf(app_name, table, fields_table, fields_pdf)
    });
}


function printPdf(app_name, table, fields_table, fields_pdf) {
    const formData = new FormData(); 
    formData.append('app_name', app_name);
    formData.append('table', table);
    fields_table.forEach(field => formData.append('fields_table[]', field));
    fields_pdf.forEach(field => formData.append('fields_pdf[]', field));

    fetch(`/print_pdf/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })
    .then(response => response.text())
    .then(html => {
        // Abrir una nueva ventana y escribir el HTML de respuesta
        const printWindow = window.open('', '_blank');
        printWindow.document.write(html);
        printWindow.document.close();

        // Agregar un script en la ventana de impresión para que se cierre después de imprimir
        printWindow.onload = () => {
            printWindow.print();
            printWindow.onafterprint = () => {
                printWindow.close();
            };
        };
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Comprobar si este cookie comienza con el nombre que buscamos
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}