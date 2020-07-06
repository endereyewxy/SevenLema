function load_orders() {
    const data = {
        page: 1,
        limit: 100
    };
    $.get('/order/info', data, (resp) => {
        paginator.maxPages = resp.page;
        $('#order-container').html($('#viewOrders-template').tmpl(resp.data));
    });
}

$(document).ready(function () {
    load_orders();
});