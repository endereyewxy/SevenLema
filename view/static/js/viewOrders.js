function load_orders() {
    const data = {
        page: paginator.currPage,
        limit:  paginator.limit
    };
    $.get('/order/info', data, (resp) => {
        paginator.maxPages = resp.page;
        $('#orders-container').html($('#viewOrders-template').tmpl(resp.data));
    });
}

$(document).ready(function () {
    paginator.change = load_orders();
    load_orders();
});