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
    for (let i =0; i < 4; i++) {
        !data.get(['name', '']).length && data.delete(['name', 'price', 'desc'][i]);
    }
    data.append('serving', $('#dish-serving:checked').length !== 0 ? 'true' : 'false');
    $.ajax({
        url: '/shop/edit',
        data: data,
        processData: false,
        contentType: false,
        type: 'post',
        success: (resp) => resp.code ? alert(resp.msg) : ($('#dish-modal').modal('hide') & load_dish())
    });
}

$(document).ready(function () {
    load_shop_info();
    $('#list-messages-list').click(load_order_info);
});



