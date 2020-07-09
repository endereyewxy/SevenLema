(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.locator = factory();
    }
}(this, function () {
    // Algorithm to decode China coordinates to real longitude and latitude.
    // Provided by https://blog.csdn.net/goodnew/article/details/82622817.
    const x_PI = 3.14159265358979324 * 3000.0 / 180.0;
    const PI = 3.1415926535897932384626, a = 6378245.0, ee = 0.00669342162296594323;

    const bd09togcj02 = (bd_lon, bd_lat) => {
        bd_lon = +bd_lon;
        bd_lat = +bd_lat;
        const x = bd_lon - 0.0065;
        const y = bd_lat - 0.006;
        const z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * x_PI);
        const theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * x_PI);
        return [z * Math.cos(theta), z * Math.sin(theta)];
    };

    const gcj02tobd09 = (lng, lat) => {
        lat = +lat;
        lng = +lng;
        const z = Math.sqrt(lng * lng + lat * lat) + 0.00002 * Math.sin(lat * x_PI);
        const theta = Math.atan2(lat, lng) + 0.000003 * Math.cos(lng * x_PI);
        return [z * Math.cos(theta) + 0.0065, z * Math.sin(theta) + 0.006];
    };

    const wgs84togcj02 = (lng, lat) => {
        lat = +lat;
        lng = +lng;
        if (out_of_china(lng, lat)) {
            return [lng, lat]
        } else {
            let d_lat = transform_lat(lng - 105.0, lat - 35.0);
            let d_lng = transform_lng(lng - 105.0, lat - 35.0);
            let rad_lat = lat / 180.0 * PI;
            let magic = Math.sin(rad_lat);
            magic = 1 - ee * magic * magic;
            const sqrt_magic = Math.sqrt(magic);
            d_lat = (d_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * PI);
            d_lng = (d_lng * 180.0) / (a / sqrt_magic * Math.cos(rad_lat) * PI);
            return [lng + d_lng, lat + d_lat];
        }
    };

    const gcj02towgs84 = (lng, lat) => {
        lat = +lat;
        lng = +lng;
        if (out_of_china(lng, lat)) {
            return [lng, lat]
        } else {
            [mglng, mglat] = wgs84togcj02(lng, lat);
            return [lng * 2 - mglng, lat * 2 - mglat];
        }
    };

    const transform_lat = (lng, lat) => {
        lat = +lat;
        lng = +lng;
        let ret = transform(lng);
        ret += -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * Math.sqrt(Math.abs(lng));
        return ret;
    };

    const transform_lng = (lng, lat) => {
        lat = +lat;
        lng = +lng;
        let ret = transform(lng);
        ret += 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * Math.sqrt(Math.abs(lng));
        return ret;
    };

    const transform = (lng) => {
        let ret = 0;
        ret += (20.0 * Math.sin(6.0 * lng * PI) + 20.0 * Math.sin(2.0 * lng * PI)) * 2.0 / 3.0;
        ret += (20.0 * Math.sin(lng * PI) + 40.0 * Math.sin(lng / 3.0 * PI)) * 2.0 / 3.0;
        ret += (150.0 * Math.sin(lng / 12.0 * PI) + 300.0 * Math.sin(lng / 30.0 * PI)) * 2.0 / 3.0;
        return ret;
    };

    const out_of_china = (lng, lat) => {
        lat = +lat;
        lng = +lng;
        return !(lng > 73.66 && lng < 135.05 && lat > 3.86 && lat < 53.55);
    };

    const html_modal =
        '<div class="modal fade" id="locator-modal" tabindex="-1" role="dialog" aria-hidden="true" style="z-index: 3000">' +
        '   <div class="modal-dialog">' +
        '       <div class="modal-content">' +
        '           <div class="modal-header"><h5 class="modal-title"></h5></div>' +
        '           <div class="modal-body" style="height: 500px" id="locator-container"></div>' +
        '           <div class="modal-footer">' +
        '               <button class="btn btn-primary" data-dismiss="modal">确定</button>' +
        '           </div>' +
        '       </div>' +
        '   </div>' +
        '</div>';
    $('html').append(html_modal);
    $('#locator-modal').on('shown.bs.modal',
        () => setTimeout(() => map.panTo(marker.getPosition()), 150));

    let lng, lat, address, map, marker, local_search, on_change = () => undefined;
    const geo_coder = new BMap.Geocoder();

    const on_location_changed = (evt) => {
        marker.setPosition(evt.point);
        geo_coder.getLocation(evt.point,
            (rs) => on_change($('#locator-modal h5').text('当前位置：' + (address = rs ? rs.address : '未知'))));
        let cvt;
        cvt = bd09togcj02(evt.point.lng, evt.point.lat);
        cvt = gcj02towgs84(cvt[0], cvt[1]);
        [lng, lat] = cvt;
    };

    const actual_create = (point) => {
        map = new BMap.Map('locator-container');
        map.centerAndZoom(point, 15);
        map.enableScrollWheelZoom();
        map.addEventListener("click", on_location_changed);
        map.addControl(new BMap.NavigationControl());
        map.addControl(new BMap.OverviewMapControl());
        map.addControl(new BMap.ScaleControl());
        map.addControl(new BMap.MapTypeControl());
        map.addControl(new BMap.CopyrightControl());
        marker = new BMap.Marker(point);
        marker.addEventListener("click", on_location_changed);
        marker.enableDragging();
        marker.addEventListener("dragend", on_location_changed);
        local_search = new BMap.LocalSearch(map, {
            renderOptions: {map: map},
            onSearchComplete:
                (result) => result.getNumPois() && on_location_changed({point: result.getPoi(0).point})
        });
        on_location_changed({point: point});
    };

    const create = (lng, lat) => {
        let geo, cvt;
        if ((geo = lng === undefined)) {
            lng = 106.30557;
            lat = 29.59899;
        }
        cvt = wgs84togcj02(lng, lat);
        cvt = gcj02tobd09(cvt[0], cvt[1]);
        const default_point = new BMap.Point(cvt[0], cvt[1]);
        geo ? (
            new BMap.Geolocation().getCurrentPosition(function (resp) {
                actual_create(this.getStatus() ? default_point : resp.point)
            }, () => actual_create(default_point))
        ) : actual_create(default_point);
    };

    const render = (addr) => {
        map.clearOverlays();
        map.addOverlay(marker);
        $('#locator-modal').modal('show');
        (typeof addr === 'string' && addr.length) && local_search.search(addr);
    };

    return {
        lng: () => lng,
        lat: () => lat,
        address: () => address,
        create: create,
        render: render,
        change: (callback) => on_change = callback
    };
}));
