let locator;

function register() {
    $('form').addClass('was-validated');
    if ($('input:invalid').length) {
        return;
    }
    const data = {
        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
        username: $('#username').val(),
        password: $('#password').val(),
        addr: $('#addr').val(),
        loc_lng: locator.lng,
        loc_lat: locator.lat,
        phone: $('#phone').val()
    };
    $.ajax({
        url: '/user/register/',
        data: data,
        type: 'post',
        success: function (data) {
            if (data.msg === 0) {
                window.location.href = "/";
            } else {
                $('#err-msg').text(data.msg).removeAttr('hidden');
            }
        }
    });
}

$(document).ready(function () {
    locator = new Locator();
    locator.change = function (lng, lat, addr) {
        $('#locator-addr').text('定位到：' + addr).removeAttr('hidden');
    };
    locator.create(106.30557, 29.59899, true);
    $('#register').click(register);
    $('#locator-show').click(function () {
        locator.show($('#addr').val());
    });
});