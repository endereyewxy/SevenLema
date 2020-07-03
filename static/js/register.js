// Initial location of Chongqing University
var v_loc_lng = 106.30557, v_loc_lat = 29.59899, v_addr = '', loc_lng = v_loc_lng, loc_lat = v_loc_lat;


function register() {
    const data = {
        "username": $('#username').val(),
        "password": $('#password').val(),
        "addr": $('#addr').val(),
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

function createMap() {
    // Create map and configure basic settings
    const map = new BMap.Map("baidu-map");
    map.setDefaultCursor("pointer");
    map.enableScrollWheelZoom();
    const point = new BMap.Point(v_loc_lng, v_loc_lat);
    map.centerAndZoom(point, 13);
    const gc = new BMap.Geocoder();

    // Add controls
    map.addControl(new BMap.NavigationControl());
    map.addControl(new BMap.OverviewMapControl());
    map.addControl(new BMap.ScaleControl());
    map.addControl(new BMap.MapTypeControl());
    map.addControl(new BMap.CopyrightControl());

    function onLocationChanged(evt) {
        v_loc_lng = evt.point.lng;
        v_loc_lat = evt.point.lat;
        gc.getLocation(evt.point, function (rs) {
            const opts = {
                width: 250,
                height: 150,
                title: "当前位置"
            };
            rs = rs.addressComponents;
            v_addr = [rs.province, rs.city, rs.district, rs.street, rs.streetNumber].join();
            $('#located').text('定位到：' + v_addr).removeAttr('hidden');
            marker.openInfoWindow(new BMap.InfoWindow(v_addr, opts));
        });
    }

    // Add marker
    const marker = new BMap.Marker(point);
    map.addOverlay(marker);
    marker.addEventListener("click", onLocationChanged);
    marker.enableDragging();
    marker.addEventListener("dragend", onLocationChanged);

    // Initialize v_addr
    onLocationChanged({point: point});
}

$(document).ready(function () {
    // Try to locate the user
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            v_loc_lng = position.longitude;
            v_loc_lat = position.latitude;
            createMap();
        }, createMap);
    } else {
        createMap();
    }
    $('#register').click(register);
    $('#confirm').click(function () {
        loc_lng = v_loc_lng;
        loc_lat = v_loc_lat;
        $('#select-location').modal('hide');
    })
});