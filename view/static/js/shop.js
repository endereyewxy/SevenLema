let page = 1, loc_lng = 0, loc_lat = 0;

function sort() {
    const order = $('label.active input').attr('id');
    const data = {
        "name": $('#header-search').val(),
        "order": order,
        "page": page,
        "limit": 5
    };
    if (order === 'dist') {
        data['loc_lng'] = loc_lng;
        data['loc_lat'] = loc_lat;
    }
    $.ajax({
        url: "/search/shop",
        data: data,
        type: "get",
        success: function (data) {
            createPages(page, data.page, function (new_page) {
                page = new_page;
                sort();
            });
            $('#container').html($('#template').tmpl(data.data));
        }
    });
}

$(document).ready(function () {
    createLocator('#locator-show', '#addr', loc_lng, loc_lat, function (lng, lat, addr) {
        $('#located').text(addr);
        loc_lng = lng;
        loc_lat = lat;
    });
    $('#header-search-button,#dist,#avg_price,#sales').click(sort);
    $('#located').click(function () {
        $('.modal').modal('show');
    });
    sort();
});
