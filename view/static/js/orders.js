function load_orders() {
    const data = {
        page: paginator.currentPage(),
        limit: paginator.limit()
    };
    miscellaneous.web.get('/order/info/', data, (resp) => {
        paginator.maximumPage(resp.page);
        $.each(resp.data, (i, data) =>
            resp.data[i].dishes = data.dishes.map((dish) => dish.name + '&times;' + dish.amount).join(', '));
        miscellaneous.loadTemplate($('#orders-container'), $('#orders-template'), resp.data);
    });
}

$(document).ready(function () {
    paginator.change(load_orders);
    load_orders();
});
