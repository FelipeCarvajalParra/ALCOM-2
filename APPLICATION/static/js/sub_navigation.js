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

        // Guardar en localStorage el ID del botón clicado
        localStorage.setItem('activeButton', this.getAttribute('data-target'));

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

// Verificar si hay un botón activo almacenado en localStorage al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const activeButtonTarget = localStorage.getItem('activeButton');
    if (activeButtonTarget) {
        // Buscar el botón que tiene el mismo atributo data-target almacenado
        const activeButton = Array.from(navButtons).find(button => button.getAttribute('data-target') === activeButtonTarget);
        
        // Simular un clic en el botón encontrado para activar la sección correcta
        if (activeButton) {
            activeButton.click();
        }
    } else {
        // Si no hay ningún botón almacenado, activar el primero por defecto
        navButtons[0].click();
    }
});
