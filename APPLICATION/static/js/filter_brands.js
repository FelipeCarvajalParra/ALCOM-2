function filterBrands() {
    var input = document.getElementById("brand").value.toLowerCase();
    var ul = document.getElementById("autocompleteListBrand");
    var li = ul.getElementsByTagName("li");
    var hasMatches = false;

    for (var i = 0; i < li.length; i++) {
        var brand = li[i].getAttribute("data-value").toLowerCase();
        if (brand.includes(input)) {
            li[i].style.display = "block"; // Muestra la marca si coincide
            hasMatches = true;
            li[i].addEventListener('click', function() {
                selectBrand(this.getAttribute('data-value')); // Llama a selectBrand al hacer clic
            });
        } else {
            li[i].style.display = "none"; // Oculta la marca si no coincide
            li[i].removeEventListener('click', selectBrand); // Elimina el evento si no coincide
        }
    }

    // Controla la visibilidad de la lista completa
    if (hasMatches && input !== "") {
        ul.style.display = "block"; // Muestra la lista si hay coincidencias
    } else {
        ul.style.display = "none"; // Oculta la lista si no hay coincidencias
    }
}

// Función para seleccionar una marca y cerrar la lista
function selectBrand(brand) {
    var input = document.getElementById("brand");
    var ul = document.getElementById("autocompleteListBrand");
    
    input.value = brand; // Coloca el valor en el input
    ul.style.display = "none"; // Oculta la lista
}