// Seleccionar todas las imágenes de vista previa
const previewImages = document.querySelectorAll('.container__image--preview');

// Seleccionar la imagen principal que se mostrará en grande
const imageDisplay = document.getElementById('image-display');

// Agregar un evento de clic a cada imagen de vista previa
previewImages.forEach(image => {
    image.addEventListener('click', function() {
        // Cambiar la fuente de la imagen principal por la fuente de la imagen seleccionada
        imageDisplay.src = this.src;
    });
});





const textareas = document.querySelectorAll('.textarea');

// Función para ajustar la altura
function adjustHeight() {

    // Ajustar la altura según el contenido
    if (this.scrollHeight > 45) {
        this.style.height = `${this.scrollHeight}px`; // Ajustar la altura al contenido
    } else {
        this.style.height = '45px'; // Mantener en 45px si el contenido es menor
    }
}

// Ajustar la altura inicial de cada textarea
textareas.forEach(textarea => {
    textarea.style.height = '45px'; // Establecer explícitamente la altura inicial
    adjustHeight.call(textarea); // Llamar a la función para configurar la altura inicial

    // Evento input para ajustar la altura conforme el usuario escribe
    textarea.addEventListener('input', adjustHeight);
});




