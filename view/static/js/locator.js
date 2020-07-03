let map, marker, geocoder, callback;

function onLocationChanged(evt) {
    marker.setPosition(evt.point);
    map.centerAndZoom(evt.point, 16);
    geocoder.getLocation(evt.point, function (rs) {
        marker.openInfoWindow(new BMap.InfoWindow(rs.address, {
            width: 250,
            height: 150,
            title: "当前位置"
        }));
        callback(evt.point.lng, evt.point.lat, rs.address);
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

function createLocator(btn, addr, def_lng, def_lat, a_callback) {
    const modal = '<div class="modal fade" id="locator-modal" tabindex="-1" role="dialog" aria-labelledby="selectLocation"\n' +
        '           aria-hidden="true">\n' +
        '               <div class="modal-dialog">\n' +
        '                   <div class="modal-content">\n' +
        '                       <div class="modal-header">\n' +
        '                           <h5 class="modal-title">选择位置</h5>\n' +
        '                       </div>\n' +
        '                       <div class="modal-body" id="baidu-map" style="height: 400px"></div>\n' +
        '                       <div class="modal-footer">\n' +
        '                           <button type="button" class="btn btn-primary" data-dismiss="modal">确定</button>\n' +
        '                       </div>\n' +
        '                   </div>\n' +
        '               </div>\n' +
        '           </div>';
    $('html').append(modal);
    callback = a_callback;
    geocoder = new BMap.Geocoder();

    // Try to locate the user
    new BMap.Geolocation().getCurrentPosition(function (resp) {
        createMap(this.getStatus() === BMAP_STATUS_SUCCESS
            ? resp.point
            : new BMap.Point(def_lng, def_lat));
    });

    $(btn).click(function () {
        $('#locator-modal').modal('show');
        let t_addr = $(addr).val();
        if (marker && t_addr !== '') {
            geocoder.getPoint(t_addr, function (point) {
                if (point) {
                    onLocationChanged({point: point});
                }
            });
        }
    });
}