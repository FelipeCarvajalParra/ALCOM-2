const modals = document.querySelectorAll('.modal');
const modalOverlay = document.querySelector('.modal-overlay');
const openModalBtns = document.querySelectorAll('[data-modal-id]');
const closeModalBtns = document.querySelectorAll('.modal__close');

// Función para abrir el modal
openModalBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const modalId = btn.getAttribute('data-modal-id');
    const modal = document.getElementById(modalId);
    
    modal.style.display = 'block'; // Primero mostramos el modal
    modalOverlay.style.display = 'block';

    // Forzamos el reflow para que CSS detecte el cambio y aplique la transición
    setTimeout(() => {
      modal.classList.add('modal--active');
      modalOverlay.classList.add('modal-overlay--active');
      document.body.classList.add('modal-open'); // Deshabilitar scroll
    }, 10); // Usamos un pequeño retraso para permitir que la transición ocurra
  });
});

// Función para cerrar el modal
closeModalBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    cerrarModal();
  });
});

// Cerrar el modal al hacer clic en el fondo oscuro
modalOverlay.addEventListener('click', () => {
  cerrarModal();
});

// Función que maneja el cierre con retraso para la animación
function cerrarModal() {
  modals.forEach(modal => {
    modal.classList.remove('modal--active');
  });
  modalOverlay.classList.remove('modal-overlay--active');
  document.body.classList.remove('modal-open'); // Habilitar scroll de nuevo

  // Esperar el tiempo de la animación antes de ocultar completamente
  setTimeout(() => {
    modals.forEach(modal => {
      modal.style.display = 'none';
    });
    modalOverlay.style.display = 'none';
  }, 300); // El tiempo debe coincidir con la duración de la transición en CSS
}