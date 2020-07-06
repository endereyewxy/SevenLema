function load_orders() {
    const data = {
        page: paginator.currentPage(),
        limit: paginator.limit()
    };

    miscellaneous.web.get('/order/info', data, (resp) => {
        paginator.maximumPage(resp.page);
        $('#orders-container').html($('#viewOrders-template').tmpl(resp.data));
    });
}

$(document).ready(function () {
    paginator.change(load_shop);
    load_orders();
});