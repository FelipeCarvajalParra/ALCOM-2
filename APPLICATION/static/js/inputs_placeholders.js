document.querySelectorAll('.input').forEach(input => {
    // Comprobar si el input ya tiene valor al cargar la página
    if (input.value !== '') {
        input.classList.add('filled');
    }

    // Añadir y quitar clase 'filled' según el valor del input
    input.addEventListener('focus', () => {
        input.classList.add('filled');
    });

    input.addEventListener('blur', () => {
        if (input.value === '') {
            input.classList.remove('filled');
        }
    });
});