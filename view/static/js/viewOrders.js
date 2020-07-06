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
    paginator.change(load_orders);
    load_orders();
});

// $(document).ready(() => {
//     paginator.change(load_shop);
//     load_orders();
//     $('#logout11').click(
//         () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
// });