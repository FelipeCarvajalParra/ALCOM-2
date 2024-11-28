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
