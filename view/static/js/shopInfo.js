let serving = false;

function load_shop_info() {
    miscellaneous.web.get('/shop/mine', {}, (resp) => {
        paginator.maximumPage(resp.page);
        miscellaneous.loadTemplate($('#shop-info-container'), $('#shop-info-template'), resp.data);
    });
}

function load_order_info(shop_id) {
    const data = {
        shop_id: shop_id,
        page: paginator.currentPage(),
        limit: paginator.limit()
    };
    miscellaneous.web.get('/order/info', data, (resp) => {
        paginator.maximumPage(resp.page);
        miscellaneous.loadTemplate($('#orders-container'), $('#orders-template'), resp.data);
    });
}

function change_shop_info(shop_id) {
    let data = new FormData(document.getElementById('change-shop-form'));

    // const loc_lng = $('input[name=loc_lng]'), loc_lat = $('input[name=loc_lat]');
    // locator.change(() => {
    //     loc_lng.val(locator.lng());
    //     loc_lat.val(locator.lat());
    //     $('#locator-addr').text('定位到：' + locator.address()).removeAttr('hidden');
    // });
    // locator.create();
    // $('#locator-show').click(() => locator.render($('input[name=addr]').val()));

    for (let i = 0; i < 4; i++) {
        !data.get(['name', 'desc', 'addr', 'phone'][i]).length && data.delete(['name', 'desc', 'addr', 'phone'][i]);
    }
    data.append('serving', $('#shop-serving:checked').length !== 0 ? 'true' : 'false')
    $.ajax({
        url: '/shop/edit',
        shop_id: shop_id,
        data: data,
        processData: false,
        contentType: false,
        type: 'post',
        success: (resp) => resp.code ? alert(resp.msg) : ($('#change-shop-modal').modal('hide') & load_shop_info())
    });
}

function change_dish_info() {
    let data = new FormData(document.getElementById('change-dish-form'));
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
        success: (resp) => resp.code ? alert(resp.msg) : ($('#change-dish-modal').modal('hide') & load_dish_info($('#change-dish-edit-id').attr('shop-id')))
    });
}


function create_dish() {
    const data = {
        shop_id: shop_id,  //
        name: $('#name').val(),
        image: $('#image').val(),
        desc: $('#desc').val,
        price: $('#price').val(),
    };
    $.ajax({
        url: '/dish/create/',
        data: data,
        processData: false,
        contentType: false,
        type: 'post',
        success: (resp) => resp.code ? alert(resp.msg) : ($('#create-dish-modal').modal('hide') & load_dish())
    });
}

function create_shop() {
    const loc_lng = $('input[name=loc_lng]'), loc_lat = $('input[name=loc_lat]');
    locator.change(() => {
        loc_lng.val(locator.lng());
        loc_lat.val(locator.lat());
        $('#locator-addr').text('定位到：' + locator.address()).removeAttr('hidden');
    });
    locator.create();
    $('#locator-show').click(() => locator.render($('input[name=addr]').val()));

    const data = {
        name: $('#name').val(),
        desc: $('#desc').val(),
        image: $('#image').val(),
        addr: $('#addr').val(),
        avg_price: $('#avg_price').val(),
        phone: $('#phone').val()
    };
    $.ajax({
        url: '/shop/create/',
        data: data,
        processData: false,
        contentType: false,
        type: 'post',
        success: (resp) => resp.code ? alert(resp.msg) : ($('#create-shop-modal').modal('hide') & load_shop_info())
    });
}

function check_order_finish() {
    data = {order_id: order_id};
    miscellaneous.web.get('/order/finish', data, (resp) => {
        $('#orders-container').html($('#orders-template').tmpl(resp.data));
    });
}

function load_dish_info(shop_id) {
    const data = {
        shop_id: shop_id,
        name: "",
        order: "sales",
        page: paginator.currentPage(),
        limit: paginator.limit(),
        serving: true
    };
    miscellaneous.web.get('/search/dish/', data, (resp) => {
        paginator.maximumPage(resp.page);
        for(let i=0;i<resp.data.length;i++){
            resp.data[i].shop_id=shop_id;
        }
        miscellaneous.loadTemplate($('#dishes-container'), $('#dishes-template'), resp.data);
    });
}

$(document).ready(() => {
    paginator.change(load_shop_info);
    load_shop_info();

    $('#change-dish-edit').click(change_dish_info);
    $('#change-dish-modal').on('show.bs.modal', (evt) => {
        $('#change-dish-edit-id')
            .val($(evt.relatedTarget).attr('id'))
            .attr('shop-id', $(evt.relatedTarget).attr('shop-id'));
    });
    $('#change-shop-edit').click(change_shop_info);
    $('#change-shop-modal').on('show.bs.modal', (evt) => $('#change-shop-edit-id').val($(evt.relatedTarget).attr('id')));
    $('#create-shop').click(create_shop);
    $('#logout').click(
        () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
});
