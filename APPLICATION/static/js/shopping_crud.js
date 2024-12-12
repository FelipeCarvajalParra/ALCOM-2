const addShoppingForm = document.getElementById('addShoppingForm');
const messageShoppingError = document.getElementById('messageShoppingError');
const idPartShopping = document.getElementById('idPart').value;
const shoppingElements = document.querySelectorAll('.passShopping');

addShoppingForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    messageShoppingError.textContent = '';

    // Crear una instancia de FormData y agregar idPartShopping
    const formData = new FormData(addShoppingForm);
    formData.append('partId', idPartShopping);

    // Enviar la solicitud con fetch
    fetch(`/new_shopping/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData // Enviar los datos del formulario
    })
    .then(response => {
        if (response.status === 403) {
            window.location.href = '/forbidden_access/';  
            return; 
        }

        return response.json();
    }) 
    .then(data => {
        if (data.error) {
            messageShoppingError.textContent = data.error;
        } else if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        messageShoppingError.textContent = 'Ha ocurrido un error en la validación.';
    });
});


shoppingElements.forEach(element => {
    element.addEventListener('click', function(event) {
        const shoppingId = element.getAttribute('data-id');
        Swal.fire({
            title: '¿Estás seguro de validar esta compra?',
            text: 'Esta acción sumará el total de partes al inventario, una vez realizada no podrás deshacer esta acción.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/validate_shopping/${shoppingId}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(response => {
                    if (response.status === 403) {
                        window.location.href = '/forbidden_access/';  
                        return; 
                    }
                    location.reload(); 
                })
            }
        });
    });
});
