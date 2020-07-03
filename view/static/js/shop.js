let paginator, locator;

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
        data['loc_lng'] = locator.lng;
        data['loc_lat'] = locator.lat;
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
    locator = new Locator();
    locator.change = function (lng, lat, addr) {
        $('#locator-addr').text(addr);
        if (get_order() === 'dist') {
            load_shop();
        }
    };
    locator.create(default_lng, default_lat);
    $('#locator-show').click(function () {
        locator.show($('#addr').val());
    });
    $('#locator-addr').click(locator.show);

    // Bind loading functions
    $('#header-search-button,#dist,#avg_price,#sales').click(load_shop);

    // Initialize settings
    load_shop();
});
