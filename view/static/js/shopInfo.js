function load_shop_info() {
    data = '';
    miscellaneous.web.get('/shop/mine', data, (resp) => {
        paginator.maximumPage(resp.page);
        $('#shopInfo-container').html($('#shopInfo-template').tmpl(resp.data));
    });
}

function create_dish() {
    const data = {
        shop_id: shop_id,
        name: $('#name').val(),
        image: $('#image').val(),
        desc: $desc('#desc').val,
        price: $('price').val(),
    };
    miscellaneous.web.get('/shop/mine', data, (resp) => {
        $('#dish-container').html($('#dish-template').tmpl(resp.data)); //
    });
}

function check_order_finish() {
    data = {order_id: order_id};
    miscellaneous.web.get('/order/finish', data, (resp) => {
        $('#data-container').html($('#data-template').tmpl(resp.data));
    });
}
$(document).ready(function () {
    paginator.change(load_shop_info);
    load_orders();
});

$(document).ready(() => {
    paginator.change(load_shop_info);
    load_orders();
    $('#logout11').click(
        () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
});