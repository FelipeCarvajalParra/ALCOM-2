document.addEventListener('DOMContentLoaded', () => {
    const optionInterventions = document.getElementById('optionInterventions')
    const interventions = document.querySelectorAll('.list-activity__intervention');
    
    function updateIntervention(interventionId) {
        const url = new URL(window.location.href);
        url.searchParams.set('intervention_id', interventionId); // Establece el parámetro intervention_id

        window.location.href = url.toString();
    }

    interventions.forEach((intervention) => {
        intervention.addEventListener('click', () => {
            const interventionId = intervention.getAttribute('data-id');
            updateIntervention(interventionId); // Redirige y recarga la página con el ID de la intervención
            optionInterventions.click()
        });
    });
});
