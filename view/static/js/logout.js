function logout() {
    $.ajax({
        url: "/user/logout",
        type: "post",
        success: function (data) {
            window.location.href = "/index.html";
        }
    });
}

$(document).ready(function () {
    $('#logout').click(logout);
});