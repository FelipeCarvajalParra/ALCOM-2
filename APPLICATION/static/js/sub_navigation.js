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

        // Obtener todos los IDs que están en los data-target de los botones
        const allTargetIds = Array.from(navButtons)
            .flatMap(btn => btn.getAttribute('data-target').split(','))
            .map(id => id.trim());

        // Ocultar todos los contenedores cuyo ID esté en la lista general de data-target
        allTargetIds.forEach(id => {
            const container = document.getElementById(id);
            if (container) {
                container.style.display = 'none';
            }
        });

        // Mostrar los contenedores correspondientes al botón clicado
        targetIds.forEach(targetId => {
            const targetContainer = document.getElementById(targetId.trim());
            if (targetContainer) {
                targetContainer.style.display = 'block'; // Mostrar el contenedor
            }
        });
    });
});

// Verificar si hay un botón activo almacenado en localStorage al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const activeButtonTarget = localStorage.getItem('activeButton');
    const currentPath = window.location.pathname; // Ruta actual

    // Solo mantener el botón activo si la URL no cambia de sección
    const previousPath = sessionStorage.getItem('previousPath');
    if (previousPath !== currentPath) {
        localStorage.removeItem('activeButton');
    }

    // Almacenar la ruta actual en sessionStorage para referencia futura
    sessionStorage.setItem('previousPath', currentPath);

    if (activeButtonTarget) {
        // Buscar el botón que tiene el mismo atributo data-target almacenado
        const activeButton = Array.from(navButtons).find(button => button.getAttribute('data-target') === activeButtonTarget);

        // Simular un clic en el botón encontrado para activar la sección correcta
        if (activeButton) {
            activeButton.click();
        }
    } else {
        if (navButtons.length > 0) {
            // Si no hay un botón activo almacenado, activar el primer botón
            navButtons[0].click();
        }
    }
});
