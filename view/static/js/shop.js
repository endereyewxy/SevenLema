let paginator, loc_lng, loc_lat;

function get_order() {
    return $('label.active input').attr('id');
}

function load_shop() {
    const data = {
        "name": $('#header-search').val(),
        "order": get_order(),
        "page": paginator.currPage,
        "limit": 5
    };
    if (get_order() === 'dist') {
        data['loc_lng'] = loc_lng;
        data['loc_lat'] = loc_lat;
    }
    $.ajax({
        url: "/search/shop",
        data: data,
        type: "get",
        success: function (data) {
            paginator.maxPages = data.page;
            $('#data-container').html($('#data-template').tmpl(data.data));
        }
    });
}

$(document).ready(function () {
    // Create and configure paginator
    paginator = new Paginator('.pagination');
    paginator.change = load_shop;

    // Create and configure locator
    let locator = new Locator();
    locator.change = function (lng, lat, addr) {
        loc_lng = lng;
        loc_lat = lat;
        if (get_order() === 'dist') {
            $('#locator-addr').text(addr);
        }
    };
    locator.create(default_lng, default_lat);
    $('#locator-show').click(locator.show);

    // Bind loading functions
    $('#header-search-button,#dist,#avg_price,#sales').click(load_shop);

    // Initialize settings
    loc_lng = default_lng;
    loc_lat = default_lat;
    load_shop();
});
