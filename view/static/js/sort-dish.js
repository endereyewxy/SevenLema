function sort_mode(shop_id, name, order, page, limit, serving) {
    const data = {
        "shop_id": shop_id,
        "name": $('#header-search').value(),
        "order": order,
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
    $('#sme-name').click(sort_mode);    //order_id
});
