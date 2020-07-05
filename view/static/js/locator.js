class Locator {
    // Please make sure that one HTML page has at most one instance!
    constructor() {
        // Add modal dialog
        const modal = '<div class="modal fade" id="locator-modal" tabindex="-1" role="dialog" aria-hidden="true">"' +
            '               <div class="modal-dialog">' +
            '                   <div class="modal-content">' +
            '                       <div class="modal-header">' +
            '                           <h5 class="modal-title"></h5>' +
            '                       </div>' +
            '                       <div class="modal-body" id="locator-map" style="height: 500px"></div>' +
            '                       <div class="modal-footer">' +
            '                           <button type="button" class="btn btn-primary" data-dismiss="modal">确定</button>' +
            '                       </div>' +
            '                   </div>' +
            '               </div>' +
            '           </div>';
        $('body').append(modal);
        const object = this;
        $('#locator-modal').on('shown.bs.modal', async function () {
            // Make sure to center the map after a short amount of time, due to unknown issues
            await new Promise(r => setTimeout(r, 150));
            object.map.panTo(object.marker.getPosition());
        });

        this.create = this.create.bind(this);
        this.show = this.show.bind(this);
        this._actual_create = this._actual_create.bind(this);
        this._on_location_changed = this._on_location_changed.bind(this);
    }

    create(default_lng, default_lat, use_geo = false) {
        // Create geo-locator
        this.geocoder = new BMap.Geocoder();

        // Actually create map
        const object = this;
        if (use_geo) {
            new BMap.Geolocation().getCurrentPosition(function (resp) {
                object._actual_create(this.getStatus() === BMAP_STATUS_SUCCESS
                    ? resp.point
                    : new BMap.Point(default_lng, default_lat));
            }, function () {
                object._actual_create(new BMap.Point(default_lng, default_lat));
            });
        } else {
            object._actual_create(new BMap.Point(default_lng, default_lat));
        }
    }

    show(addr) {
        // Remove markers added by the previous searching
        this.map.clearOverlays();
        this.map.addOverlay(this.marker);

        $('#locator-modal').modal('show');
        if (typeof addr === 'string' && addr.length) {
            this.local.search(addr);
        }
    }

    get lng() {
        return this.marker.getPosition().lng;
    }

    get lat() {
        return this.marker.getPosition().lat;
    }

    _actual_create(point) {
        // Create map and configure basic settings
        this.map = new BMap.Map("locator-map");
        this.map.centerAndZoom(point, 15);
        this.map.enableScrollWheelZoom();
        this.map.addEventListener("click", this._on_location_changed);
        this.map.addControl(new BMap.NavigationControl());
        this.map.addControl(new BMap.OverviewMapControl());
        this.map.addControl(new BMap.ScaleControl());
        this.map.addControl(new BMap.MapTypeControl());
        this.map.addControl(new BMap.CopyrightControl());

        // Add marker
        this.marker = new BMap.Marker(point);
        this.marker.addEventListener("click", this._on_location_changed);
        this.marker.enableDragging();
        this.marker.addEventListener("dragend", this._on_location_changed);

        // Add local searcher
        const object = this;
        this.local = new BMap.LocalSearch(this.map, {
            renderOptions: {map: this.map},
            onSearchComplete: function (result) {
                if (result.getNumPois()) {
                    object._on_location_changed({point: result.getPoi(0).point});
                }
            }
        });

        // Initialize address display
        this._on_location_changed({point: point});
    }

    _on_location_changed(evt) {
        this.marker.setPosition(evt.point);
        const object = this;
        this.geocoder.getLocation(evt.point, function (rs) {
            const addr = rs ? rs.address : '未知';
            $('#locator-modal h5').text('当前位置：' + addr);
            object.change(evt.point.lng, evt.point.lat, addr);
        });
    }
}
