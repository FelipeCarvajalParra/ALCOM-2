const aside = document.querySelector('.aside');
const asideInfo = document.querySelector('.aside-nav-info-user');
const links = document.querySelectorAll('.aside__nav-item-link');
const chevrons = document.querySelectorAll('.aside__nav-item-chevron');
const main = document.querySelector('.main');
const btnClose = document.getElementById('aside__close-btn');
const prueba = document.querySelectorAll('.aside__nav-option-sublist');

// Alternar el sidebar
function toggleSidebar(isContracted) {
    prueba.forEach(i => {
        i.style.transition = 'none';
    });

    // Remover la clase 'active' de todas las sublistas abiertas
    const subListActive = document.querySelectorAll('.aside__nav-option-sublist--active');
    subListActive.forEach(subItem => {
        subItem.classList.remove('aside__nav-option-sublist--active');
    });

    // Remover la clase 'aside__nav-item-chevron--active' de todos los chevrons activos
    const chevronsActive = document.querySelectorAll('.aside__nav-item-chevron--active');
    chevronsActive.forEach(chevron => {
        chevron.classList.remove('aside__nav-item-chevron--active');
    });

    // Remover la clase 'aside__nav-item--active' de todos los ítems activos
    const navItemsActive = document.querySelectorAll('.aside__nav-item--active');
    navItemsActive.forEach(navItem => {
        navItem.classList.remove('aside__nav-item--active');
    });

    // Alternar la clase 'aside--contract' en el sidebar
    aside.classList.toggle('aside--contract', isContracted);
    
    // Ajustar la visibilidad de la información de usuario y los enlaces del menú
    asideInfo.style.display = isContracted ? 'none' : 'block';
    
    // Alternar la visibilidad de los elementos (enlaces y chevrons)
    toggleVisibility([...links, ...chevrons], !isContracted);

    main.style.width = 'calc(100% - 65px)';

    if (isContracted) {
        aside.style.position = 'absolute';
    }

    prueba.forEach(i => {
        i.style.transition = '';
    });

    // Comprobar las sublistas
    const subLists = document.querySelectorAll('.aside__nav-option-sublist');
    subLists.forEach(subList => {
        const currentItem = subList.querySelector('.aside__nav-item--current');
        if (currentItem) {
            subList.classList.add('aside__nav-option-sublist--active');
        } else {
            subList.classList.remove('aside__nav-option-sublist--active');
        }
    });
}

// Alternar visibilidad de elementos
function toggleVisibility(elements, show) {
    elements.forEach(element => {
        element.style.display = show ? 'block' : 'none';
    });
}

// Manejar el clic en los elementos del menú
function handleNavItemClick() {
    const subList = this.nextElementSibling; // Detecta la sublista siguiente

    // Cerrar cualquier sublista activa si se hace clic en otro elemento
    document.querySelectorAll('.aside__nav-option-sublist--active').forEach(openSubList => {
        if (openSubList !== subList) {
            openSubList.classList.remove('aside__nav-option-sublist--active');
            openSubList.previousElementSibling.classList.remove('aside__nav-item--active');
            const chevron = openSubList.previousElementSibling.querySelector('.aside__nav-item-chevron');
            if (chevron) {
                chevron.classList.remove('aside__nav-item-chevron--active');
            }
        }
    });

    var sideWidth = window.getComputedStyle(aside).width;

    if (parseFloat(sideWidth) >= 66) {
        if (subList && subList.classList.contains('aside__nav-option-sublist')) {
            subList.classList.toggle('aside__nav-option-sublist--active');
            this.classList.toggle('aside__nav-item--active');

            // Verificar si existe el chevron y añadir/remover clase
            const chevron = this.querySelector('.aside__nav-item-chevron');
            if (chevron) {
                chevron.classList.toggle('aside__nav-item-chevron--active');
            }
        }
    } else {
        if (subList && subList.classList.contains('aside__nav-option-sublist')) {
            const isContracted = aside.classList.contains('aside--contract');
            toggleSidebar(!isContracted);
            subList.classList.toggle('aside__nav-option-sublist--active');
            this.classList.toggle('aside__nav-item--active');
            
            // Verificar si existe el chevron y añadir/remover clase
            const chevron = this.querySelector('.aside__nav-item-chevron');

            if (chevron) {
                chevron.classList.toggle('aside__nav-item-chevron--active');
            }
        }
    }
}

// Asignar manejadores de eventos
const navItems = document.querySelectorAll('.aside__nav-item');
navItems.forEach(navItem => navItem.addEventListener('click', handleNavItemClick));

// Manejar cambios de pantalla
function handleScreenChange(event) {
    const isSmallScreen = event.matches;
    
    toggleSidebar(isSmallScreen);

    main.style.marginLeft = isSmallScreen ? '65px' : '0';
    aside.style.position = isSmallScreen ? 'absolute' : 'static';
}

// Media query para pantallas pequeñas
const mediaQuery = window.matchMedia('(max-width: 1000px)');
handleScreenChange(mediaQuery); // Estado inicial
mediaQuery.addEventListener('change', handleScreenChange); // Escuchar cambios

btnClose.addEventListener('click', () => {
    toggleSidebar(true);
});

// Esto se debe ejecutar una vez al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const subLists = document.querySelectorAll('.aside__nav-option-sublist');

    subLists.forEach(subList => {
        const currentItem = subList.querySelector('.aside__nav-item--current');
        if (currentItem) {
            subList.classList.add('aside__nav-option-sublist--active');
            const navItem = subList.previousElementSibling;
            if (navItem) {
                navItem.classList.add('aside__nav-item--active');
                const chevron = navItem.querySelector('.aside__nav-item-chevron');
                if (chevron) {
                    chevron.classList.add('aside__nav-item-chevron--active');
                }
            }
        }
    });
});
