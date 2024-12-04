document.querySelectorAll('.movement').forEach(movement => {

    const movemenDate = document.getElementById('movemenDate');
    const movementQuantity = document.getElementById('movementQuantity');
    const movementObservations = document.getElementById('movementObservations');
    const movementSource = document.getElementById('movementSource');
    const movemenAction = document.getElementById('movemenAction');
    
    movemenDate.textContent = '';
    movementQuantity.textContent = '';
    movementObservations.textContent = '';
    movementSource.textContent = '';
    movemenAction.textContent = '';
    
    movement.addEventListener('click', function() {
        const movementId = this.getAttribute('data-id');

        fetch(`/consult_movements/${movementId}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {

            if (data.movement[0].type_movement == 'Entrada') {
                movemenAction.textContent = 'ingreso';
            } else if (data.movement[0].type_movement == 'Salida') {
                movemenAction.textContent = 'egreso';
            }

            movemenDate.textContent = data.movement[0].date;
            movementQuantity.textContent = data.movement[0].amount;
            

            movementObservations.textContent = data.movement[0].observations;
            movementSource.textContent = data.movement[0].source;
        })
    });
});