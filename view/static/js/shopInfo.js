const load_shop_info = () => {
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
        $('#data-container').html($('#data-template').tmpl(resp.data));
    });
};
