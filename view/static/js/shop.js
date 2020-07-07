let serving = false;

const load_shop = () => {
    const data = {
        name: $('#header-search').val(),
        order: get_order(),
        page: paginator.currentPage(),
        limit: paginator.limit(),
        serving: serving
    };
    if (get_order() === 'dist') {
        data['loc_lng'] = locator.lng;
        data['loc_lat'] = locator.lat;
    }
    miscellaneous.web.get('/search/shop/', data, (resp) => {
        paginator.maximumPage(resp.page);
        miscellaneous.loadTemplate($('#data-container'), $('#data-template'), resp.data);
    });
};

$(document).ready(function () {
    paginator.change(load_shop);
    locator.change(() => {
        $('#locator-addr').text(locator.address);
        get_order() === 'dist' && load_shop();
    });
    default_lng !== undefined ? locator.create(default_lng, default_lat) : locator.create();
    $('#header-search-button,#dist,#avg_price,#sales').click(load_shop);
    load_shop();
});
