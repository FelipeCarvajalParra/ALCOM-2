function searchUsers() {
    var search = $('#searchUser').val();

    $.ajax({
        url: '/view_users/',
        data: {
            'search': search
        },
        success: function(data) {
            $('.table__body').html(data);
        }
    });
}

let timeout;

$('#searchUser').on('input', function() {
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        searchUsers();
    }, 150); // Ajusta el tiempo según tus necesidades
});