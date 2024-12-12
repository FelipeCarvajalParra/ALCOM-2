const movemenDate = document.getElementById('movemenDate');
const movementQuantity = document.getElementById('movementQuantity');
const movementObservations = document.getElementById('movementObservations');
const movementSource = document.getElementById('movementSource');
const movemenAction = document.getElementById('movemenAction');

const shoppinPartName = document.getElementById('shoppinPartName');
const shoppinPartCode = document.getElementById('shoppinPartCode');
const shoppinDate = document.getElementById('shoppinDate');
const shoppingQuantity = document.getElementById('shoppingQuantity');
const shoppingColor = document.getElementById('shoppingColor');
const shoppingObservations = document.getElementById('shoppingObservations');

function modalMovements(){
    document.querySelectorAll('.movement').forEach(movement => {
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



    document.querySelectorAll('.shopping').forEach(movement => {
        shoppinDate.textContent = '';
        shoppingQuantity.textContent = '';
        shoppingColor.textContent = '';
        shoppingObservations.textContent = '';
        
        movement.addEventListener('click', function() {
            const shoppingId = this.getAttribute('data-id');
    
            fetch(`/consult_shopping/${shoppingId}`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                shoppinPartName.textContent = data.shopping.partName; 
                shoppinPartCode.textContent = data.shopping.partNumber;
                shoppinDate.textContent = data.shopping.date;         
                shoppingQuantity.textContent = data.shopping.amount; 
                shoppingColor.textContent = data.shopping.color;     
                shoppingObservations.textContent = data.shopping.observations; 
            })
            .catch(error => {
                console.error("Error procesando la respuesta del servidor:", error);
            });
        });
    });
};


document.addEventListener('DOMContentLoaded', function() {
    modalMovements();
});
  
