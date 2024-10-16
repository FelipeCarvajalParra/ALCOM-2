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










