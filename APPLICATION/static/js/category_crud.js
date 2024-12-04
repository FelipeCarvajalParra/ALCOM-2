// Obtener referencias a los elementos del formulario
const form = document.getElementById('newCategoryForm');
const nameCategory = document.getElementById('nameCategory');
const componentsList = document.getElementById('componentsList');
const messageError = document.getElementById('messageError');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    messageError.textContent = '‎'; // Limpiar cualquier mensaje de error previo

    // Recoger los componentes seleccionados
    const components = [];
    document.querySelectorAll('.task-text').forEach(item => {
        components.push(item.textContent.trim());
    });

    const uniqueComponents = [...new Set(components)];

    const formData = {
        nameCategory: nameCategory.value.trim(),
        components: uniqueComponents
    };

    // Hacer una solicitud POST al servidor
    fetch('/new_categorie/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        // Si el estado es 403, redirigir manualmente
        if (response.status === 403) {
            window.location.href = '/forbidden_access/';  // Redirige a la página de acceso denegado
            return; // Salir de la promesa
        }

        // Si la respuesta no es 403, procesamos la respuesta JSON
        return response.json();
    })
    .then(data => {
        if (data) {  // Verifica si hay datos válidos
            if (data.error) {
                messageError.textContent = data.error;  // Muestra el error
            } else if (data.success) {
                // Recargar la página si la categoría fue creada con éxito
                location.reload();
            }
        }
    })
    .catch(error => {
        messageError.textContent = 'Ha ocurrido un error en la validación.';  // Muestra un mensaje de error
    });
});

// Obtener referencias a los elementos del formulario de actualización
const editForm = document.getElementById('editCategoryForm');
const editNameCategory = document.getElementById('editNameCategory');
const editComponentsList = document.getElementById('editComponentsList');
const editMessageError = document.getElementById('editMessageError');

editForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    editMessageError.textContent = '‎'; // Limpiar cualquier mensaje de error previo

    // Recoger los componentes seleccionados
    const components = [];
    document.querySelectorAll('#editComponentsList .task-text').forEach(item => {
        components.push(item.textContent.trim());
    });

    const uniqueComponents = [...new Set(components)];

    const formData = {
        nameCategory: editNameCategory.value.trim(),
        components: uniqueComponents
    };

    // Obtener el ID de la categoría
    const categoryId = document.getElementById('editCategoryId').value;

    // Hacer una solicitud POST al servidor
    fetch(`/update_category/${categoryId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        // Si el estado es 403, redirigir manualmente
        if (response.status === 403) {
            window.location.href = '/forbidden_access/';  // Redirige a la página de acceso denegado
            return; // Salir de la promesa
        }

        // Si la respuesta no es 403, procesamos la respuesta JSON
        return response.json();
    })
    .then(data => {
        if (data) {  // Verifica si hay datos válidos
            if (data.error) {
                editMessageError.textContent = data.error;  // Muestra el error
            } else if (data.success) {
                // Recargar la página o cerrar el modal si la categoría fue actualizada con éxito
                location.reload();
            }
        }
    })
    .catch(error => {
        editMessageError.textContent = 'Ha ocurrido un error en la validación.';  // Muestra un mensaje de error
    });
});

