// Inicialización de tooltips para los botones flotantes
const optionsTooltips = document.querySelectorAll('.floating-button__link');
optionsTooltips.forEach(option => {
    tippy(option, {
        content: option.dataset.tooltip,  // Contenido del tooltip
        placement: 'left',                // Posición del tooltip
        animation: 'scale',               // Animación de escala
        theme: 'custom-tooltip',          // Tema
        offset: [0, 10],                  // Desplazamiento del tooltip
        duration: [0, 0],                 // [entrada, salida] en milisegundos
        arrow: true
    });
});

document.querySelectorAll('.floating-button__link').forEach(button => {
    // Detectar cuando termina la animación de entrada (slideIn)
    button.addEventListener('animationend', (event) => {
        // Verificar si la animación es la de entrada (slideIn)
        if (event.animationName === 'slideIn') {
            button.classList.add('visible'); // Habilitar la interacción
        }
    });

    // También se puede agregar una animación de salida si se desea manipular la salida de manera similar
    button.addEventListener('animationstart', (event) => {
        if (event.animationName === 'fadeOut') {
            button.classList.remove('visible'); // Deshabilitar la interacción al inicio de la animación de salida
        }
    });
});

