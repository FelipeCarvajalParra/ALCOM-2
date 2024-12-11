let counter = 1;
        
// Selecciona el contenedor donde se agregarán las nuevas intervenciones
const elementNewPart = document.getElementById('elementNewPart');
const container = document.getElementById('container');
const messageNewInterventionError = document.getElementById('messageNewInterventionError');
const codeEquipment = document.getElementById('codeEquipment').textContent;

// Función para agregar la funcionalidad del ícono de eliminar
function addDeleteEventListener(clone) {
    const closeIcon = clone.querySelector('.container__close-icon');
    closeIcon.addEventListener('click', function () {
        clone.remove();
    });
}

// Función para clonar y agregar una nueva intervención
document.getElementById('buttonNewPart').addEventListener('click', function () {
    const clone = elementNewPart.cloneNode(true);

    // Asignar IDs únicos a los elementos del clon
    const inputs = clone.querySelectorAll('input');
    inputs.forEach(input => {
        input.id = input.name + counter;
        input.name = input.name + counter;
        input.value = ''; // Resetear valores
    });

    const textareas = clone.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.id = textarea.name + counter;
        textarea.value = ''; // Resetear valores
    });

    const labels = clone.querySelectorAll('label');
    labels.forEach(label => {
        const forAttr = label.getAttribute('for');
        if (forAttr) {
            label.setAttribute('for', forAttr + counter);
        }
    });

    // Reiniciar el campo select de "Acción"
    const actionSelect = clone.querySelector('.select__selected');
    if (actionSelect) {
        actionSelect.textContent = 'Accion';
    }

    // Agregar evento de eliminar al nuevo clon
    addDeleteEventListener(clone);

    // Añadir el clon al contenedor
    container.appendChild(clone);

    // Añadir event listeners a los nuevos selects
    const newSelectElements = clone.querySelectorAll('.select--filter');
    newSelectElements.forEach(selectElement => {
        addEventListenersToSelectElement(selectElement);
    });

    // Asegurarse de que los textareas tengan la altura adecuada y los placeholders estén activos
    heightTextareas();
    placeholders();

    // Incrementar el contador para el siguiente clon
    counter++;
});

// Añadir evento de eliminar al ícono inicial
addDeleteEventListener(elementNewPart);

document.getElementById('saveButton').addEventListener('click', function (event) {
    // Prevenir el envío del formulario
    messageNewInterventionError.textContent = '';
    event.preventDefault();

    const result = [];

    // Recoger datos de cada intervención
    const parts = document.querySelectorAll('.container__update-part');
    parts.forEach(part => {
        const partData = {
            part: part.querySelector('input[name^="part"]').value,
            amount: part.querySelector('input[name^="amount"]').value,
            observations: part.querySelector('textarea[name^="observations"]').value,
            action: part.querySelector('.select__selected').textContent
        };
        result.push(partData);
    });

    // Obtener Observaciones Generales
    const generalObservations = document.querySelector('textarea[name="generalObservations"]').value;

    // Obtener Procedimiento
    const procedure = document.querySelector('.select--intervention .select__selected').textContent;

    // Almacenar todo en un objeto
    const dataToSave = {
        procedure,
        generalObservations,
        interventions: result, 
        codeEquipment
    };

    // Enviar los datos al backend con fetch
    fetch('/new_intervention/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(dataToSave) // Convertir el objeto a JSON
    })
    .then(response => {
        if (response.status === 403) {
            window.location.href = '/forbidden_access/';  
            return; 
        }
        return response.json();
    }) 
    .then(data => {
        if (data.error) {
            messageNewInterventionError.textContent = data.error;
        }else{
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageNewInterventionError.textContent = 'Ha ocurrido un error en la validación.';
    });
});

