function login() {
    const data = {
        "username": $('#username').val(),
        "password": $('#password').val()
    };
    $.ajax({
        url: "/user/login",
        data: data,
        type: "post",
        success: function (data) {
            if (data.code === 0) {
                window.location.href = "/index.html";
            } else {
                $('#alert').text(data.msg).removeAttr('hidden');
            }
        }
    });
}

$(document).ready(function () {
    $('#login').click(login);
});