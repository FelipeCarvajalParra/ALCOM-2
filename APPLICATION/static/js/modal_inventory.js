// Inicializar variables fuera del forEach
const partModalName = document.getElementById('partModalName');
const partModalNumber = document.getElementById('partModalNumber');
const partModalLocation = document.getElementById('partModalLocation');
const partModalStock = document.getElementById('partModalStock');
const partModalLink = document.getElementById('partModalLink');
const partModalManual = document.getElementById('partModalManual');

// Limpiar contenido y estilos iniciales
partModalName.textContent = '';
partModalNumber.textContent = '';
partModalLocation.textContent = '';
partModalStock.textContent = '';
partModalLink.style.display = 'block';
partModalManual.style.display = 'block';
partModalLink.href = '';
partModalManual.href = '';

document.querySelectorAll('.part').forEach(movement => {
    movement.addEventListener('click', function() {
        const partId = this.getAttribute('data-id');

        fetch(`/consult_part/${partId}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {


            console.log(data);

            partModalName.textContent = data.part.name;
            partModalNumber.textContent = data.part.number;
            partModalLocation.textContent = data.part.location;
            partModalStock.textContent = data.part.stock;

            if (data.part.url) {
                partModalLink.href = data.part.url;
                partModalLink.style.display = 'block';
            } else {
                partModalLink.style.display = 'none';
            }

            if (data.part.manual) {
                partModalManual.href = data.part.manual;
                partModalManual.style.display = 'block';
            } else {
                partModalManual.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error al consultar la parte. Por favor, inténtalo de nuevo.');
        });
    });
});