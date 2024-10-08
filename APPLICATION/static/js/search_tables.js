function updateEquipos() {
    var search = $('#searchUser').val();

    $.ajax({
        url: '/view_users/',
        data: {
            'search': search
        },
        success: function(data) {
            // Actualiza el contenido del cuerpo de la tabla con el nuevo HTML
            $('.table__body').html(data);
        }
    });
}

let timeout;

$('#searchUser').on('input', function() {
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        updateEquipos();
    }, 1000); // Ajusta el tiempo según tus necesidades
});