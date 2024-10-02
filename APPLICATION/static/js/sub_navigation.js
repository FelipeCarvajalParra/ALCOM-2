// Selecciona todos los botones de navegación
const navButtons = document.querySelectorAll('.button--navegation');

// Función para manejar el click en los botones
navButtons.forEach(button => {
    button.addEventListener('click', function () {
        // Remover la clase 'button--active' de todos los botones
        navButtons.forEach(btn => btn.classList.remove('button--active'));

        // Añadir la clase 'button--active' al botón actual
        this.classList.add('button--active');

        // Obtener los IDs de los contenedores objetivos desde el atributo 'data-target'
        const targetIds = this.getAttribute('data-target').split(',');

        // Ocultar todos los contenedores con la clase 'container--activity'
        document.querySelectorAll('.container--activity').forEach(container => {
            container.style.display = 'none';
        });

        // Mostrar todos los contenedores correspondientes al botón clicado
        targetIds.forEach(targetId => {
            const targetContainer = document.getElementById(targetId.trim());
            if (targetContainer) {
                targetContainer.style.display = 'block';  // Asegurar que se muestre
            }
        });
    });
});
