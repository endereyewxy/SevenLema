class Locator {
    // Please make sure that one HTML page has at most one instance!
    constructor() {
        // Add modal dialog
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

        // Create map and configure basic settings
        this.map = new BMap.Map("baidu-map");
        this.map.setDefaultCursor("pointer");
        this.map.enableScrollWheelZoom();

        // Add controls
        this.map.addControl(new BMap.NavigationControl());
        this.map.addControl(new BMap.OverviewMapControl());
        this.map.addControl(new BMap.ScaleControl());
        this.map.addControl(new BMap.MapTypeControl());
        this.map.addControl(new BMap.CopyrightControl());

        // Create geo-locator
        this.geocoder = new BMap.Geocoder();
    }

    create(default_lng = 106.30557, default_lat = 29.59899, use_geo = false) {
        const object = this;
        if (use_geo) {
            new BMap.Geolocation().getCurrentPosition(function (resp) {
                object._actual_create(this.getStatus() === BMAP_STATUS_SUCCESS
                    ? resp.point
                    : new BMap.Point(default_lng, default_lat));
            }, function () {
                object._actual_create(new BMap.Point(default_lng, default_lat));
            });
        }
    }

    show(addr) {
        $('#locator-modal').modal('show');
        if (addr) {
            const object = this;
            this.geocoder.getPoint(addr, function (point) {
                if (point) {
                    object._on_location_changed({point: point});
                }
            });
        }
    }

    change() {
    }

    _actual_create(point) {
        // Add marker
        this.marker = new BMap.Marker(point);
        this.map.addOverlay(this.marker);
        this.marker.addEventListener("click", this._on_location_changed);
        this.marker.enableDragging();
        this.marker.addEventListener("dragend", this._on_location_changed);

        // Add click event listener to the map
        this.map.addEventListener("click", this._on_location_changed);

        // Initialize address display
        this._on_location_changed({point: point});
    }

    _on_location_changed() {
        this.marker.setPosition(evt.point);
        this.map.centerAndZoom(evt.point);

        const object = this;
        this.geocoder.getLocation(evt.point, function (rs) {
            object.marker.openInfoWindow(new BMap.InfoWindow(rs.address, {
                width: 250,
                height: 150,
                title: "当前位置"
            }));
            object.change(evt.point.lng, evt.point.lat, rs.address);
        });
    }
}
