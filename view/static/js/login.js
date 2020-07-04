function login() {
    const data = {
        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
        username: $('#username').val(),
        password: $('#password').val()
    };
    $.ajax({
        url: "/user/login/",
        data: data,
        type: 'post',
        success: function (data) {
            if (data.code === 0) {
                window.location.href = '/';
            } else {
                $('#alert').text(data.msg).removeAttr('hidden');
            }
        }
    });
}

$(document).ready(function () {
    $('#login').click(login);
});