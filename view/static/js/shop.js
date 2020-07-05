let paginator, locator, serving = false;

function get_order() {
    return $('label.active input').attr('id');
}
2
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
    if (default_lng !== undefined) {
        locator.create(default_lng, default_lat);
    } else {
        locator.create(106.30557, 29.59899, true);
    }
    const html =
        '<div class="popover" role="tooltip">' +
        '   <div class="arrow"></div>' +
        '   <h3 class="popover-header"></h3>' +
        '   <div>' +
        '       <input type="checkbox" id="serving" onchange="serving = $(\'#serving:checked\').length === 1;load_shop();">' +
        '       <label for="serving">只显示营业中的商家</label>' +
        '   </div>' +
        '</div>'
    $('#header-config-button').popover({
        content: () => $($('#serving-wrapper').html().replace('hidden', '').replace('-1', '')),
        placement: 'bottom',
        trigger: 'click',
        html: true
    });
    $('#locator-show').click(function () {
        locator.show($('#addr').val());
    });
    $('#locator-addr').click(locator.show);

    // Bind loading functions
    $('#header-search-button,#dist,#avg_price,#sales').click(load_shop);

    // Initialize settings
    load_shop();
});
