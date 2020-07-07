function load_orders() {
    const data = {
        page: paginator.currentPage(),
        limit: paginator.limit()
    };
    miscellaneous.web.get('/order/info', data, (resp) => {
        paginator.maximumPage(resp.page);
        miscellaneous.loadTemplate($('#orders-container'), $('#orders-template'), resp.data);
    });
}

$(document).ready(function () {
    paginator.change(load_orders);
    load_orders();
    $('#logout').click(
        () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
});
