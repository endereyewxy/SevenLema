let map, marker, geocoder;


function register() {
    const data = {
        "username": $('#username').val(),
        "password": $('#password').val(),
        "addr": $('#addr').val(),
        "loc_lng": marker.getPosition().longitude,
        "loc_lat": marker.getPosition().latitude,
        "phone": $('#phone').val()
    };
    $.ajax({
        url: "/user/register",
        data: data,
        type: "post",
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
    let locator = new Locator();
    locator.change = function (lng, lat, addr) {
        $('#locator-addr').text(addr)
    };
    geocoder = new BMap.Geocoder();
    // Try to locate the user
    new BMap.Geolocation().getCurrentPosition(function (resp) {
        createMap(this.getStatus() === BMAP_STATUS_SUCCESS
            ? resp.point
            : new BMap.Point(106.30557, 29.59899)); // Set to Chongqing University's location by default
    });
    $('#register').click(register);
    $('#locator-show').click(function () {
        $('#locator-modal').modal('show');
        let addr = $('#addr').val();
        if (marker && addr !== '') {
            geocoder.getPoint(addr, function (point) {
                if (point) {
                    onLocationChanged({point: point});
                }
            });
        }
    });
});