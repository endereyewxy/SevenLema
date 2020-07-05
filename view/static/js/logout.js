function logout() {
    $.ajax({
        url: '/user/logout/',
        data: {csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()},
        type: 'post',
        success: function (data) {
            window.location.href = "/"; // TODO
        }
    });
}

$(document).ready(function () {
    $('#logout').click(logout);
});