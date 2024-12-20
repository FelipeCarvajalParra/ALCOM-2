const printUsersExcel = document.getElementById('printUsersExcel');
const printEquipmentsExcel = document.getElementById('printEquipmentsExcel');
const printReferencesExcel = document.getElementById('printReferencesExcel');

if (printUsersExcel) {
    printUsersExcel.addEventListener('click', function () {
        const app_name = 'users';
        const table = 'customUser';
        const fields_table = [ 'first_name', 'last_name', 'username', 'email', 'position'];
        const fields_pdf = [ 'Nombres', 'Apellidos', 'Usuario', 'Correo', 'Cargo'];
        downloadExcel(app_name, table, fields_table, fields_pdf);
    });
}

if (printEquipmentsExcel) {
    printEquipmentsExcel.addEventListener('click', function () {
        const app_name = 'equipments';
        const table = 'equipos';
        const fields_table = ['referencia_fk.referencia_pk', 'referencia_fk.marca' ,'cod_equipo_pk', 'serial', 'estado'];
        const fields_pdf = ['Referencia', 'Marca', 'Codigo ALCOM', 'Serial', 'Estado'];
        downloadExcel(app_name, table, fields_table, fields_pdf);
    });
}

if (printReferencesExcel) {
    printReferencesExcel.addEventListener('click', function () {
        const app_name = 'references';
        const table = 'referencias';
        const fields_table = ['categoria', 'referencia_pk' ,'marca'];
        const fields_pdf = ['Categoria', 'Referencia', 'Marca', ];
        downloadExcel(app_name, table, fields_table, fields_pdf);
    });
}

function downloadExcel(app_name, table, fields_table, fields_pdf) {
    const formData = new FormData(); 
    formData.append('app_name', app_name);
    formData.append('table', table);
    fields_table.forEach(field => formData.append('fields_table[]', field));
    fields_pdf.forEach(field => formData.append('fields_pdf[]', field));

    fetch(`/print_excel/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Error en la generación del archivo Excel');
    })
    .then(blob => {
        // Crear un enlace de descarga para el archivo
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'registros.xlsx';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    })
}
