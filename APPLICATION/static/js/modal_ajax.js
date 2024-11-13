document.querySelectorAll('.movement').forEach(movement => {

    const movemenDate = document.getElementById('movemenDate');
    const movementQuantity = document.getElementById('movementQuantity');
    const movementObservations = document.getElementById('movementObservations');
    const movementSource = document.getElementById('movementSource');

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
            movemenDate.textContent = data.movement[0].date;
            movementQuantity.textContent = data.movement[0].amount;
            movementObservations.textContent = data.movement[0].observations;
            movementSource.textContent = data.movement[0].source;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});