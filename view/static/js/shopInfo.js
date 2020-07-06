let serving = false;

function load_shop_info() {
    const data = { };
    miscellaneous.web.get('/shop/mine', data, (resp) => {
        paginator.maximumPage(resp.page);
        miscellaneous.loadTemplate($('#shop-info-container'), $('#shop-info-template'), resp.data);
    });
}

function load_order_info() {
    const data = {};
    miscellaneous.web.get('/order/info', data, (resp) => {
        paginator.maximumPage(resp.page);
        $('#list-messages').html($('#viewOrders-template').tmpl(resp.data));
        miscellaneous.loadTemplate($('#orders-container'), $('#orders-template'), resp.data);
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

    for (let i = 0; i < 4; i++) {
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

function change_dish_info() {
    let data = new FormData(document.getElementById('dish-form'));
    for (let i = 0; i < 3; i++) {
        !data.get(['name', 'price', 'desc'][i]).length && data.delete(['name', 'price', 'desc'][i]);
    }
    data.append('serving', $('#dish-serving:checked').length !== 0 ? 'true' : 'false');
    $.ajax({
        url: '/dish/edit/',
        data: data,
        processData: false,
        contentType: false,
        type: 'post',
        success: (resp) => resp.code ? alert(resp.msg) : ($('#dish-modal').modal('hide') & load_dish())
    });
}


function create_dish() {
    const data = {
        shop_id: shop_id,  //
        name: $('#name').val(),
        image: $('#image').val(),
        desc: $('#desc').val,
        price: $('price').val(),
    };
    miscellaneous.web.get('/dish/create', data, (resp) => {
        paginator.maximumPage(resp.page);
        miscellaneous.loadTemplate($('#dishes-container'), $('#dishes-info-template'), resp.data);
    });
}

function check_order_finish() {
    data = {order_id: order_id};
    miscellaneous.web.get('/order/finish', data, (resp) => {
        $('#orders-container').html($('#orders-template').tmpl(resp.data));
    });
}



$(document).ready(() => {
    $('#logout').click(
        () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
});

$(document).ready(function () {
    load_shop_info();
    $('#list-messages-list').click(load_order_info);
});




