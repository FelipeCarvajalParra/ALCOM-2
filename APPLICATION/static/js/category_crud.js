// Obtener referencias a los elementos del formulario
const form = document.getElementById('newCategoryForm');
const nameCategory = document.getElementById('nameCategory');
const componentsList = document.getElementById('componentsList');
const messageError = document.getElementById('messageError');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    messageError.textContent = '‎';

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
    .then(response => response.json()) // Procesar la respuesta como JSON
    .then(data => {
        if (data.error) {
            messageError.textContent = data.error;
        } else if (data.success) {
            // Recargar la página si la categoría fue creada con éxito
            location.reload();

        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageError.textContent = 'Ha ocurrido un error en la validación.';
    });
});

// Obtener referencias a los elementos del formulario de actualización
const editForm = document.getElementById('editCategoryForm');
const editNameCategory = document.getElementById('editNameCategory');
const editComponentsList = document.getElementById('editComponentsList');
const editMessageError = document.getElementById('editMessageError');

editForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    editMessageError.textContent = '‎';

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
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            editMessageError.textContent = data.error;
        } else if (data.success) {
            // Recargar la página o cerrar el modal si la categoría fue actualizada con éxito
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        editMessageError.textContent = 'Ha ocurrido un error en la validación.';
    });
});

