function load_shop_info() {
    const data = {
        page: paginator.currPage,
        limit: paginator.limit
    };
    miscellaneous.web.get('/shop/mine', data, (resp) => {
        paginator.maximumPage(resp.page);
        $('#info-container').html($('#info-template').tmpl(resp.data));
    });
}

function load_order_info() {
    const data = {
        page: paginator.currPage,
        limit: paginator.limit
    };
    miscellaneous.web.get('/order/info', data, (resp) => {
        paginator.maximumPage(resp.page);
        $('#list-messages').html($('#viewOrders-template').tmpl(resp.data));
    });
}

function change_shop_info() {
    let data = new FormData(document.getElementById('shop-form'));

    const loc_lng = $('input[name=loc_lng]'), loc_lat = $('input[name=loc_lat]');
    locator.change(() => {
        loc_lng.val(locator.lng());
        loc_lat.val(locator.lat());
        $('#locator-addr').text('定位到：' + locator.address()).removeAttr('hidden');
    });
    locator.create();
    $('#locator-show').click(() => locator.render($('input[name=addr]').val()));

    for (let i =0; i < 4; i++) {
        !data.get(['name', 'desc', 'addr', 'phone', 'image']).length && data.delete(['name', 'desc', 'addr', 'phone', 'image'][i]);
    }
    data.append('serving', $('#shop-serving:checked').length !== 0 ? 'true' : 'false');
    $.ajax({
        url: '/shop/edit',
        data: data,
        processData: false,
        contentType: false,
        type: 'post',
        success: (resp) => resp.code ? alert(resp.msg) : ($('#shopModal').modal('hide') & load_dish())
    });
}

function create_shop(name, image, desc, addr, loc_lng, loc_lat, avg_price, phone) {



}




$(document).ready(function () {
    load_shop_info();
    $('#list-messages-list').click(load_order_info);
});



