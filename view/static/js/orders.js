let pager;

function load_orders() {
    const data = {
        page: pager.currentPage(),
        limit: pager.limit()
    };
    miscellaneous.web.get('/order/info/', data, (resp) => {
        pager.maximumPage(resp.page);
        $.each(resp.data, (i, data) =>
            resp.data[i].dishes = data.dishes.map((dish) => dish.name + '&times;' + dish.amount).join(', '));
        miscellaneous.loadTemplate($('#orders-container'), $('#orders-template'), resp.data);
    });
}

$(document).ready(function () {
    pager = paginator.create($('.pagination'));
    pager.change(load_orders);
    load_orders();
});
