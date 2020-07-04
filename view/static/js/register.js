let locator;

function register() {
    const data = {
        username: $('#username').val(),
        password: $('#password').val(),
        addr: $('#addr').val(),
        loc_lng: locator.lng,
        loc_lat: locator.lat,
        phone: $('#phone').val()
    };
    $.ajax({
        url: '/user/register',
        data: data,
        type: 'post',
        success: function (data) {
            if (data.msg === 0) {
                window.location.href = "/index.html";
            } else {
                $('#alert').text(data.msg).removeAttr('hidden');
            }
        }
    });
}

$(document).ready(function () {
    locator = new Locator();
    locator.change = function (lng, lat, addr) {
        $('#locator-addr').text(addr).removeAttr('hidden');
    };
    locator.create(106.30557, 29.59899, true);
    $('#register').click(register);
    $('#locator-show').click(function () {
        locator.show($('#addr').val());
    });
});