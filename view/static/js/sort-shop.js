function sort_mode(name, order, loc_lng, loc_lat, tags, page, limit, serving) {
    const data = {
        "name": $('#header-search').value(),
        "order": order,
        "loc_lng": loc_lng,
        "loc_lat": loc_lat,
        "tags": tags,
        "page": page,
        "limit": limit,
        "serving": serving
    };
    $.ajax({
        url: "/search/shop",
        data: data,
        type: "get",
        success: function (data) {
            const num = data.page;    // TODO
            $('#each').tmpl(data.data).appendTo('#eachList');
        }
    });
}

$(document).load(function () {
    $('#header-search-button').click(sort_mode);
    $('#sme-name').click(sort_mode);
});
