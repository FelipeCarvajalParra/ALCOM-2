document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('taskInput');
    const taskList = document.getElementById('taskList');
    const taskListAutocomplete = document.getElementById('taskList__autocomplete');

    // Evento para añadir una nueva tarea
    document.getElementById('addButton').addEventListener('click', function () {
        const taskValue = taskInput.value.trim();

        // Validación para no agregar duplicados
        if (taskValue && !isTaskDuplicate(taskValue)) {
            // Crear un nuevo elemento de lista
            const listItem = document.createElement('li');
            listItem.className = 'task-item';
            listItem.innerHTML = `
                <span class="task-text">${taskValue}</span>
                <button type="button" class="deleteButton">Eliminar</button>
            `;

            // Añadir evento para eliminar
            listItem.querySelector('.deleteButton').addEventListener('click', function () {
                taskList.removeChild(listItem);
            });

            taskList.appendChild(listItem);
            taskInput.value = ''; // Limpiar el campo de entrada
            hideOptions(); // Ocultar las opciones después de añadir
        }
    });

    // Función para verificar si la tarea ya está en la lista
    function isTaskDuplicate(taskValue) {
        const tasks = document.querySelectorAll('.task-text');
        for (let task of tasks) {
            if (task.textContent.toLowerCase() === taskValue.toLowerCase()) {
                return true; // Si encuentra una coincidencia
            }
        }
        return false;
    }

    // Función para mostrar la lista de coincidencias
    function showOptions() {
        taskListAutocomplete.style.display = 'block';
    }

    // Función para ocultar la lista de coincidencias
    function hideOptions() {
        taskListAutocomplete.style.display = 'none';
    }

    // Filtrar las opciones según la entrada del usuario
    taskInput.addEventListener('input', function() {
        const filter = taskInput.value.trim().toLowerCase();
        const options = taskListAutocomplete.querySelectorAll('li');
        let hasVisibleOption = false; // Variable para rastrear si hay alguna opción visible
        
        options.forEach(option => {
            const optionText = option.textContent.toLowerCase();
            if (optionText.includes(filter)) {
                option.style.display = 'block'; // Mostrar la opción si coincide
                hasVisibleOption = true; // Marcar como visible
            } else {
                option.style.display = 'none'; // Ocultar la opción si no coincide
            }
        });

        // Mostrar la lista solo si hay opciones visibles
        if (hasVisibleOption) {
            showOptions();
        } else {
            hideOptions(); // Ocultar si no hay coincidencias
        }
    });

    // Manejar la selección de una opción en la lista de autocompletado
taskListAutocomplete.addEventListener('click', function(event) {
const target = event.target;
if (target.tagName === 'LI') {
    const newTaskValue = target.getAttribute('data-value') || target.textContent; // Obtener el valor de la opción
    
    // Validación para no agregar duplicados
    if (!isTaskDuplicate(newTaskValue)) {
        const listItem = document.createElement('li');
        listItem.className = 'task-item';
        listItem.innerHTML = `
            <span class="task-text">${newTaskValue}</span>
            <svg class="svg-option svg-option--delete deleteButton" width="20px" height="20px">
                <use href="#icon-delete"></use>
            </svg>
        `;
        taskList.appendChild(listItem);
        taskInput.value = ''; // Limpiar el campo de entrada
        hideOptions(); // Ocultar las opciones después de añadir

        // Añadir evento para eliminar el nuevo elemento
        listItem.querySelector('.deleteButton').addEventListener('click', function () {
            taskList.removeChild(listItem);
        });
    } else {
        taskInput.value = ''; // Limpiar el campo si es duplicado
        hideOptions(); // Ocultar las sugerencias si no se añade
    }
}
});

    // Ocultar opciones al hacer clic fuera del campo de entrada
    document.addEventListener('click', function(event) {
        if (!taskInput.contains(event.target) && !taskListAutocomplete.contains(event.target)) {
            hideOptions();
        }
    });
});