function searchCategories() {
    var search = $('#searchCategories').val();

    $.ajax({
        url: '/view_categories/',
        data: {
            'search': search
        },
        success: function(data) {
            $('.table__body').html(data);
        }
    });
}

let timeout;

$('#searchCategories').on('input', function() {
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        searchCategories();
    }, 500); // Ajusta el tiempo según tus necesidades
});