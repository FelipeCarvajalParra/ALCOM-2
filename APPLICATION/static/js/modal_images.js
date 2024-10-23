 // Obtener el modal y la imagen que se mostrará
 var modal = document.getElementById("modal");
 var modalImg = document.getElementById("modalImage");
 var imageDisplay = document.getElementById("image-display");

 // Obtener todas las imágenes de la galería
 var images = document.querySelectorAll(".container__image--preview");
 var currentIndex = 0;

 // Actualizar la imagen principal al hacer clic en la miniatura
 images.forEach((img, index) => {
     img.onclick = function() {
         imageDisplay.src = this.src; // Cambiar la imagen principal
         currentIndex = index; // Guardar el índice actual
     }
 });

 // Abrir el modal al hacer clic en el enlace "Ver en grande"
 var expandedImageLink = document.getElementById("expandedImage");
 expandedImageLink.onclick = function(e) {
     e.preventDefault(); // Prevenir el comportamiento predeterminado del enlace
     modal.style.display = "flex";
     modalImg.src = imageDisplay.src; // Mostrar la imagen actual en el modal
 }

 // Cerrar el modal
 var closeBtn = document.querySelector(".modal-image__close");
 closeBtn.onclick = function() {
     modal.style.display = "none";
     modalImg.classList.remove("modal-image__image--zoomed");
 }

 // Funciones para el carrusel
 var prevBtn = document.querySelector(".modal-image__button--prev");
 var nextBtn = document.querySelector(".modal-image__button--next");

 prevBtn.onclick = function() {
     currentIndex = (currentIndex - 1 + images.length) % images.length;
     updateModalImage();
 }

 nextBtn.onclick = function() {
     currentIndex = (currentIndex + 1) % images.length;
     updateModalImage();
 }

 function updateModalImage() {
     modalImg.src = images[currentIndex].src;
     modalImg.classList.remove("modal-image__image--zoomed");
 }

 // Hacer zoom cuando se hace clic en la imagen dentro del modal
 modalImg.onclick = function() {
     if (modalImg.classList.contains("modal-image__image--zoomed")) {
         modalImg.classList.remove("modal-image__image--zoomed");
     } else {
         modalImg.classList.add("modal-image__image--zoomed");
     }
 }

 // Cerrar el modal al hacer clic fuera de la imagen
 window.onclick = function(event) {
     if (event.target == modal) {
         modal.style.display = "none";
         modalImg.classList.remove("modal-image__image--zoomed");
     }
 }