// Algorithm source: https://blog.csdn.net/goodnew/article/details/82622817

//定义一些常量
const x_PI = 3.14159265358979324 * 3000.0 / 180.0;
const PI = 3.1415926535897932384626;
const a = 6378245.0;

const ee = 0.00669342162296594323;
/**
 * 百度坐标系 (BD-09) 与 火星坐标系 (GCJ-02)的转换
 * 即 百度 转 谷歌、高德
 * @param bd_lon
 * @param bd_lat
 * @returns {*[]}
 */
const bd09togcj02 = function bd09togcj02(bd_lon, bd_lat) {
    bd_lon = +bd_lon;
    bd_lat = +bd_lat;
    const x = bd_lon - 0.0065;
    const y = bd_lat - 0.006;
    const z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * x_PI);
    const theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * x_PI);
    const gg_lng = z * Math.cos(theta);
    const gg_lat = z * Math.sin(theta);
    return [gg_lng, gg_lat]
};

/**
 * 火星坐标系 (GCJ-02) 与百度坐标系 (BD-09) 的转换
 * 即谷歌、高德 转 百度
 * @param lng
 * @param lat
 * @returns {*[]}
 */
const gcj02tobd09 = function gcj02tobd09(lng, lat) {
    lat = +lat;
    lng = +lng;
    const z = Math.sqrt(lng * lng + lat * lat) + 0.00002 * Math.sin(lat * x_PI);
    const theta = Math.atan2(lat, lng) + 0.000003 * Math.cos(lng * x_PI);
    const bd_lng = z * Math.cos(theta) + 0.0065;
    const bd_lat = z * Math.sin(theta) + 0.006;
    return [bd_lng, bd_lat]
};

/**
 * WGS84转GCj02
 * @param lng
 * @param lat
 * @returns {*[]}
 */
const wgs84togcj02 = function wgs84togcj02(lng, lat) {
    lat = +lat;
    lng = +lng;
    if (out_of_china(lng, lat)) {
        return [lng, lat]
    } else {
        let dlat = transformlat(lng - 105.0, lat - 35.0);
        let dlng = transformlng(lng - 105.0, lat - 35.0);
        const radlat = lat / 180.0 * PI;
        let magic = Math.sin(radlat);
        magic = 1 - ee * magic * magic;
        const sqrtmagic = Math.sqrt(magic);
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI);
        dlng = (dlng * 180.0) / (a / sqrtmagic * Math.cos(radlat) * PI);
        const mglat = lat + dlat;
        const mglng = lng + dlng;
        return [mglng, mglat]
    }
};

/**
 * GCJ02 转换为 WGS84
 * @param lng
 * @param lat
 * @returns {*[]}
 */
const gcj02towgs84 = function gcj02towgs84(lng, lat) {
    lat = +lat;
    lng = +lng;
    if (out_of_china(lng, lat)) {
        return [lng, lat]
    } else {
        let dlat = transformlat(lng - 105.0, lat - 35.0);
        let dlng = transformlng(lng - 105.0, lat - 35.0);
        const radlat = lat / 180.0 * PI;
        let magic = Math.sin(radlat);
        magic = 1 - ee * magic * magic;
        const sqrtmagic = Math.sqrt(magic);
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI);
        dlng = (dlng * 180.0) / (a / sqrtmagic * Math.cos(radlat) * PI);
        const mglat = lat + dlat;
        const mglng = lng + dlng;
        return [lng * 2 - mglng, lat * 2 - mglat]
    }
};

const transformlat = function transformlat(lng, lat) {
    lat = +lat;
    lng = +lng;
    let ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * Math.sqrt(Math.abs(lng));
    ret += (20.0 * Math.sin(6.0 * lng * PI) + 20.0 * Math.sin(2.0 * lng * PI)) * 2.0 / 3.0;
    ret += (20.0 * Math.sin(lat * PI) + 40.0 * Math.sin(lat / 3.0 * PI)) * 2.0 / 3.0;
    ret += (160.0 * Math.sin(lat / 12.0 * PI) + 320 * Math.sin(lat * PI / 30.0)) * 2.0 / 3.0;
    return ret
};

const transformlng = function transformlng(lng, lat) {
    lat = +lat;
    lng = +lng;
    let ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * Math.sqrt(Math.abs(lng));
    ret += (20.0 * Math.sin(6.0 * lng * PI) + 20.0 * Math.sin(2.0 * lng * PI)) * 2.0 / 3.0;
    ret += (20.0 * Math.sin(lng * PI) + 40.0 * Math.sin(lng / 3.0 * PI)) * 2.0 / 3.0;
    ret += (150.0 * Math.sin(lng / 12.0 * PI) + 300.0 * Math.sin(lng / 30.0 * PI)) * 2.0 / 3.0;
    return ret
};

/**
 * 判断是否在国内，不在国内则不做偏移
 * @param lng
 * @param lat
 * @returns {boolean}
 */
const out_of_china = function out_of_china(lng, lat) {
    lat = +lat;
    lng = +lng;
    // 纬度3.86~53.55,经度73.66~135.05
    return !(lng > 73.66 && lng < 135.05 && lat > 3.86 && lat < 53.55);
};

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
        this.geocoder = new BMap.Geocoder();

        this.create = this.create.bind(this);
        this.show = this.show.bind(this);
        this._actual_create = this._actual_create.bind(this);
        this._on_location_changed = this._on_location_changed.bind(this);
    }

    create(default_lng, default_lat, use_geo = false) {
        // Actually create map
        let cvt = wgs84togcj02(default_lng, default_lat);
        cvt = gcj02tobd09(cvt[0], cvt[1]);
        const object = this, default_point = new BMap.Point(cvt[0], cvt[1]);
        if (use_geo) {
            new BMap.Geolocation().getCurrentPosition(function (resp) {
                object._actual_create(this.getStatus() === BMAP_STATUS_SUCCESS
                    ? resp.point
                    : default_point);
            }, function () {
                object._actual_create(default_point);
            });
        } else {
            object._actual_create(default_point);
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
        let cvt = bd09togcj02(evt.point.lng, evt.point.lat);
        cvt = gcj02towgs84(cvt[0], cvt[1]);
        this.lng = cvt[0];
        this.lat = cvt[1];
    }
}
