document.addEventListener('DOMContentLoaded', function () {
    const modals = [
        {
            taskInput: document.getElementById('taskInput'),
            componentsList: document.getElementById('componentsList'),
            autocompleteList: document.getElementById('autocompleteListNewCategory'),
            addButton: document.getElementById('addButton'),
            errorMessage: document.getElementById('messageError'),
            addTask: function (taskValue) {
                if (taskValue && !isTaskDuplicate(this.componentsList, taskValue)) {
                    const listItem = createListItem(taskValue);
                    this.componentsList.appendChild(listItem);
                    this.taskInput.value = ''; // Limpiar el campo de entrada
                    hideOptions(this.autocompleteList); // Ocultar las opciones después de añadir
                    this.errorMessage.textContent = '';
                } else {
                    this.errorMessage.textContent = 'El campo ya está asociado.';
                }
            }
        },
        {
            taskInput: document.getElementById('editTaskInput'),
            componentsList: document.getElementById('editComponentsList'),
            autocompleteList: document.getElementById('autocompleteListUpdateCategory'),
            addButton: document.getElementById('editAddButton'),
            errorMessage: document.getElementById('editMessageError'),
            addTask: function (taskValue) {
                if (taskValue && !isTaskDuplicate(this.componentsList, taskValue)) {
                    const listItem = createListItem(taskValue);
                    this.componentsList.appendChild(listItem);
                    this.taskInput.value = ''; // Limpiar el campo de entrada
                    hideOptions(this.autocompleteList); // Ocultar las opciones después de añadir
                    this.errorMessage.textContent = '';
                } else {
                    this.errorMessage.textContent = 'El campo ya está asociado.';
                }
            }
        }
    ];

    // Manejar eventos de añadir atributos
    modals.forEach(modal => {
        modal.addButton.addEventListener('click', function () {
            modal.addTask(modal.taskInput.value.trim());
        });

        modal.autocompleteList.addEventListener('click', function (event) {
            const target = event.target;
            if (target.tagName === 'LI') {
                const newTaskValue = target.getAttribute('data-value') || target.textContent;
                modal.addTask(newTaskValue); // Añadir automáticamente la tarea
                hideOptions(modal.autocompleteList); // Cerrar la lista de opciones después de seleccionar
            }
        });

        modal.taskInput.addEventListener('input', function () {
            const filter = modal.taskInput.value.trim().toLowerCase();
            const options = modal.autocompleteList.querySelectorAll('li');
            let hasVisibleOption = false;

            options.forEach(option => {
                const optionText = option.textContent.toLowerCase();
                if (optionText.includes(filter)) {
                    option.style.display = 'block';
                    hasVisibleOption = true;
                } else {
                    option.style.display = 'none';
                }
            });

            if (hasVisibleOption) {
                showOptions(modal.autocompleteList);
            } else {
                hideOptions(modal.autocompleteList);
            }
        });
    });

    // Función para crear un nuevo elemento de lista
    function createListItem(taskValue) {
        const listItem = document.createElement('li');
        listItem.className = 'task-item';
        listItem.innerHTML = `
            <span class="task-text">${taskValue}</span>
            <svg class="svg-option svg-option--delete deleteButton" width="20px" height="20px">
                <use href="#icon-delete"></use>
            </svg>
        `;
        listItem.querySelector('.deleteButton').addEventListener('click', function () {
            const parentList = listItem.parentNode;
            parentList.removeChild(listItem);
        });
        return listItem;
    }

    // Función para verificar si la tarea ya está en la lista
    function isTaskDuplicate(componentsList, taskValue) {
        const tasks = componentsList.querySelectorAll('.task-text');
        for (let task of tasks) {
            if (task.textContent.toLowerCase() === taskValue.toLowerCase()) {
                return true; // Si encuentra una coincidencia
            }
        }
        return false;
    }

    // Función para mostrar la lista de coincidencias
    function showOptions(autocompleteList) {
        autocompleteList.style.display = 'block';
        autocompleteList.setAttribute('aria-hidden', 'false');
    }

    // Función para ocultar la lista de coincidencias
    function hideOptions(autocompleteList) {
        autocompleteList.style.display = 'none';
        autocompleteList.setAttribute('aria-hidden', 'true');
    }

    // Ocultar opciones al hacer clic fuera del campo de entrada
    document.addEventListener('click', function (event) {
        const outsideClick = !modals.some(modal =>
            modal.taskInput.contains(event.target) ||
            modal.autocompleteList.contains(event.target)
        );

        if (outsideClick) {
            modals.forEach(modal => hideOptions(modal.autocompleteList));
        }
    });
});

document.querySelectorAll('.editCategoryButton').forEach(svg => {
    svg.addEventListener('click', function () {
        const categoryId = this.getAttribute('data-category-id'); 

        this.setAttribute('data-modal-id', 'modalEditCategory');

        fetch(`/get_category/${categoryId}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('editCategoryId').value = data.categoria_pk; // Cargar ID de la categoría
                document.getElementById('editNameCategory').value = data.nombre; // Cargar nombre de la categoría

                // Cargar campos existentes en la lista
                const editComponentsList = document.getElementById('editComponentsList');
                editComponentsList.innerHTML = ''; // Limpiar la lista anterior

                data.campos.forEach(campo => {
                    const li = document.createElement('li');

                    // Crear el HTML del campo con estilo
                    li.className = 'task-item';
                    li.innerHTML = `
                        <span class="task-text">${campo.nombre_campo}</span>
                        <svg class="svg-option svg-option--delete deleteButton" width="20px" height="20px">
                            <use href="#icon-delete"></use>
                        </svg>
                    `;

                    editComponentsList.appendChild(li);

                    // Añadir evento para eliminar el campo (solo visual)
                    li.querySelector('.deleteButton').addEventListener('click', function () {
                        li.remove();
                    });

                });

            });
    });
});

// Selecciona todos los botones de cerrar modal
const closeModalButtons = document.querySelectorAll('.modal__close');
const modalOverlays = document.querySelectorAll('.modal-overlay');

// Función para limpiar la lista de componentes
function clearEditComponentsList() {
    document.getElementById('editComponentsList').innerHTML = ''; // Limpia la lista de componentes
}

// Añadir listener a los botones de cerrar modal
closeModalButtons.forEach(button => {
    button.addEventListener('click', clearEditComponentsList);
});

// Añadir listener a los overlays de modal
modalOverlays.forEach(overlay => {
    overlay.addEventListener('click', clearEditComponentsList);
});