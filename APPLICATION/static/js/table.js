document.addEventListener("DOMContentLoaded", function() {
    const cells = document.querySelectorAll('.table__cell--overflow');

    let activeTooltip = null; // Variable para guardar el tooltip activo

    cells.forEach(cell => {
        cell.addEventListener('mouseenter', function() {
            const tooltipText = cell.getAttribute('data-text');
            
            // Elimina el tooltip anterior si existe
            if (activeTooltip) {
                activeTooltip.remove();
                activeTooltip = null;
            }

            // Crea el nuevo tooltip
            const tooltip = document.createElement('div');
            tooltip.classList.add('table__tooltip');
            tooltip.textContent = tooltipText;

            // Añade el tooltip al body
            document.body.appendChild(tooltip);
            activeTooltip = tooltip; // Guarda el tooltip activo

            // Obtén las dimensiones de la celda y el tooltip
            const rect = cell.getBoundingClientRect();
            const tooltipRect = tooltip.getBoundingClientRect();

            // Posición inicial debajo de la celda con separación positiva
            let topPosition = rect.bottom + window.scrollY - 15; // Justo debajo de la celda (5px de espacio)
            let leftPosition = rect.left + window.scrollX;

            // Verifica si hay espacio suficiente debajo de la celda
            const spaceBelow = window.innerHeight - rect.bottom;
            const spaceAbove = rect.top;

            // Si no cabe abajo, lo coloca arriba
            if (spaceBelow < tooltipRect.height && spaceAbove >= tooltipRect.height) {
                topPosition = rect.top + window.scrollY - tooltipRect.height - 15; // Coloca el tooltip arriba con separación negativa
            }

            // Verifica si el tooltip se desborda por la derecha de la pantalla
            if (leftPosition + tooltipRect.width > window.innerWidth) {
                leftPosition = window.innerWidth - tooltipRect.width - 10; // Ajusta para que no se desborde
            }

            // Aplica las posiciones
            tooltip.style.top = `${topPosition}px`;
            tooltip.style.left = `${leftPosition}px`;

            // Muestra el tooltip
            tooltip.classList.add('table__tooltip--visible');

            // Remueve el tooltip al salir del mouse
            cell.addEventListener('mouseleave', function() {
                tooltip.remove();
                activeTooltip = null; // Resetea la variable para futuros tooltips
            });
        });
    });
});

