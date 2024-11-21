document.addEventListener('DOMContentLoaded', () => {

    const interventions = document.querySelectorAll('.list-activity__intervention');
    
    // Añadir el evento de clic para cada intervención
    interventions.forEach(intervention => {
        intervention.addEventListener('click', () => {
            const interventionId = intervention.getAttribute('data-id'); // Obtén el ID de la intervención

            fetch(`/consult_interventions/${interventionId}`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al obtener los datos del servidor');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error(data.error); // Maneja errores desde el servidor
                    return;
                }

                // Actualiza el contenedor principal con el nuevo contenido
                const interventionContainers = document.querySelector('#interventionContainers');
                if (interventionContainers && data.body) {
                    const tempContainer = document.createElement('div');
                    tempContainer.innerHTML = data.body; // Inserta el HTML en un contenedor temporal
                    const newContent = tempContainer.firstElementChild; // Obtiene el nodo con el nuevo contenido
                    interventionContainers.replaceWith(newContent); // Reemplaza el contenido principal
                } else {
                    console.error('No se encontró el contenedor principal o el contenido está vacío.');
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
            });
        });
    });

});
