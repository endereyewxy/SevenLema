let serving = false;

const get_order = () => $('.btn-group input:checked').attr('id');

function load_shop() {
    const data = {
        name: $('#header-search').val(),
        order: get_order(),
        page: paginator.currPage,
        limit: paginator.limit,
        serving: serving
    };
    if (get_order() === 'dist') {
        data['loc_lng'] = locator.lng;
        data['loc_lat'] = locator.lat;
    }
    $.get("/search/shop", data, (resp) => {
        paginator.maxPages = resp.page;
        $('#data-container').html($('#data-template').tmpl(resp.data));
    });
}

$(document).ready(function () {
    paginator.change = load_shop;
    locator.change = (lng, lat, addr) => {
        $('#locator-addr').text(addr);
        get_order() === 'dist' && load_shop();
    };
    default_lng !== undefined ? locator.create(default_lng, default_lat) : locator.create(106.30557, 29.59899, true);
    $('#header-search-button,#dist,#avg_price,#sales').click(load_shop);
    load_shop();
});
