let timeoutReferences;

function petition(url, search) {
    let data = {
        'search': search,
    };

    return $.ajax({
        url: url,
        data: data,
        method: 'GET',
    }).then(response => {
        $('.container__references').html(response.body);
        $('.table__footer').html(data.footer);
    });
}

$(document).on('input', '#inputSearchReferences', function() {
    clearTimeout(timeoutReferences);
    timeout = setTimeout(function() {
        const inputSearchReferences = $('#inputSearchReferences').val();
        petition('/view_all_references/', inputSearchReferences);
    }, 350);
}); 