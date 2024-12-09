document.addEventListener('DOMContentLoaded', () => {
    const optionInterventions = document.getElementById('optionInterventions')
    const interventions = document.querySelectorAll('.list-activity__intervention');
    
    // Función para manejar el cambio de intervención
    function updateIntervention(interventionId) {
        const url = new URL(window.location.href);
        url.searchParams.set('intervention_id', interventionId); // Establece el parámetro intervention_id

        // Realiza la redirección a la nueva URL (esto recargará la página)
        window.location.href = url.toString();
    }

    // Añadir el evento de clic para cada intervención
    interventions.forEach((intervention) => {
        intervention.addEventListener('click', () => {
            const interventionId = intervention.getAttribute('data-id'); // Obtén el ID de la intervención
            updateIntervention(interventionId); // Redirige y recarga la página con el ID de la intervención
            optionInterventions.click()
        });
    });
});
