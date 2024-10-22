const previews = document.querySelectorAll('.container__image--preview');
const mainImage = document.getElementById('image-display');
const fileUploadInput = document.getElementById('equipmentFileImageInput');

// Agrega un evento de clic a cada miniatura
previews.forEach(preview => {
    preview.addEventListener('click', () => {
        // Cambia la imagen principal por la ruta de la miniatura seleccionada
        mainImage.src = preview.src;

        // Actualiza el atributo `data-field` e `data-record` del input

        fileUploadInput.setAttribute('data-field', preview.id); // Cambia el data-field por el ID de la imagen seleccionada

    });
});









