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

function onLocationChanged(evt) {
    marker.setPosition(evt.point);
    map.centerAndZoom(evt.point, 16);
    geocoder.getLocation(evt.point, function (rs) {
        marker.openInfoWindow(new BMap.InfoWindow(rs.address, {
            width: 250,
            height: 150,
            title: "当前位置"
        }));
        $('#located').text('定位到：' + rs.address).removeAttr('hidden');
    });
}

function createMap(point) {
    // Create map and configure basic settings
    map = new BMap.Map("baidu-map");
    map.setDefaultCursor("pointer");
    map.enableScrollWheelZoom();
    map.centerAndZoom(point, 13);

    // Add controls
    map.addControl(new BMap.NavigationControl());
    map.addControl(new BMap.OverviewMapControl());
    map.addControl(new BMap.ScaleControl());
    map.addControl(new BMap.MapTypeControl());
    map.addControl(new BMap.CopyrightControl());

    // Add marker
    marker = new BMap.Marker(point);
    map.addOverlay(marker);
    marker.addEventListener("click", onLocationChanged);
    marker.enableDragging();
    marker.addEventListener("dragend", onLocationChanged);

    // Add click event listener to the map
    map.addEventListener("click", onLocationChanged);

    // Initialize address display
    onLocationChanged({point: point});
}

$(document).ready(function () {
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