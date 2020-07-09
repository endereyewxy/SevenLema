let serving = false, pager, dish_pagers, order_pagers;

function load_shop_info() {
    dish_pagers = {};
    order_pagers = {};
    miscellaneous.web.get('/shop/mine/', {}, (resp) => {
        pager.maximumPage(resp.page);
        miscellaneous.loadTemplate($('#shop-info-container'), $('#shop-info-template'), resp.data, false, (data) => {
            const shop_id = data.shop_id;
            dish_pagers[shop_id] = paginator.create($('#dish-pager-' + shop_id));
            dish_pagers[shop_id].change(() => load_dish_info(shop_id));
            order_pagers[shop_id] = paginator.create($('#order-pager-' + shop_id));
            order_pagers[shop_id].change(() => load_order_info(shop_id));
        });
    });
}

function load_dish_info(shop_id) {
    const data = {
        shop_id: shop_id,
        name: '',
        order: 'sales',
        page: dish_pagers[shop_id].currentPage(),
        limit: dish_pagers[shop_id].limit()
    };
    miscellaneous.web.get('/search/dish/', data, (resp) => {
        dish_pagers[shop_id].maximumPage(resp.page);
        for (let i = 0; i < resp.data.length; i++) {
            resp.data[i].shop_id = shop_id;
        }
        miscellaneous.loadTemplate($('#dishes-container-' + shop_id), $('#dishes-template'), resp.data);
    });
}


function load_order_info(shop_id) {
    const data = {
        shop_id: shop_id,
        page: order_pagers[shop_id].currentPage(),
        limit: order_pagers[shop_id].limit()
    };
    miscellaneous.web.get('/order/info/', data, (resp) => {
        order_pagers[shop_id].maximumPage(resp.page);
        $.each(resp.data, (i, data) =>
            resp.data[i].dishes = data.dishes.map((dish) => dish.name + '&times;' + dish.amount).join(', '));
        miscellaneous.loadTemplate($('#orders-container-' + shop_id), $('#orders-template'), resp.data);
    });
}

function change_shop_info() {
    $('#change-shop-form').addClass('was-validated');
    if (!$('#change-shop-form input:invalid').length) {
        let data = new FormData(document.getElementById('change-shop-form'));
        $.each(['name', 'desc', 'addr', 'phone', 'avg_price', 'image'], (_, key) => {
            !data.get(key).length && data.delete(key);
            return true;
        });
        if (!data.get('addr')) {
            data.delete('loc_lng');
            data.delete('loc_lat');
        }
        data.append('serving', $('#shop-serving:checked').length !== 0 ? 'true' : 'false');
        $.ajax({
            url: '/shop/edit/',
            data: data,
            processData: false,
            contentType: false,
            type: 'post',
            success: (resp) => resp.code
                ? miscellaneous.alert(resp.msg)
                : ($('#change-shop-modal').modal('hide') & load_shop_info())
        });
    }
}

function change_dish_info() {
    $('#change-dish-form').addClass('was-validated');
    if (!$('#change-dish-form input:invalid').length) {
        let data = new FormData(document.getElementById('change-dish-form'));
        $.each(['name', 'price', 'desc', 'image'], (_, key) => {
            !data.get(key).length && data.delete(key);
            return true;
        });
        data.append('serving', $('#dish-serving:checked').length !== 0 ? 'true' : 'false');
        $.ajax({
            url: '/dish/edit/',
            data: data,
            processData: false,
            contentType: false,
            type: 'post',
            success: (resp) => resp.code
                ? miscellaneous.alert(resp.msg)
                : ($('#change-dish-modal').modal('hide') & load_dish_info($('#change-dish-id').attr('shop-id')))
        });
    }
}


function create_dish() {
    $('#create-dish-form').addClass('was-validated');
    if (!$('#create-dish-form input:invalid').length) {
        const data = new FormData(document.getElementById('create-dish-form'));
        $.ajax({
            url: '/dish/create/',
            data: data,
            processData: false,
            contentType: false,
            type: 'post',
            success: (resp) => resp.code
                ? miscellaneous.alert(resp.msg)
                : ($('#create-dish-modal').modal('hide') & load_dish_info(Number(data.get('shop_id'))))
        });
    }
}

function create_shop() {
    $('#create-shop-form').addClass('was-validated');
    if (!$('#create-shop-form input:invalid').length) {
        $.ajax({
            url: '/shop/create/',
            data: new FormData(document.getElementById('create-shop-form')),
            processData: false,
            contentType: false,
            type: 'post',
            success: (resp) => resp.code
                ? miscellaneous.alert(resp.msg)
                : ($('#create-shop-modal').modal('hide') & load_shop_info())
        });
    }
}

function finish_order_commit() {
    miscellaneous.web.post('/order/finish/', {order_id: $(this).attr('order-id')},
        () => $('#finish-order-modal').modal('hide') & load_order_info(Number($(this).attr('shop-id'))));
}


$(document).ready(() => {
    pager = paginator.create($('#global-pager'));
    pager.change(load_shop_info);
    load_shop_info();
    const loc_lng = $('input[name=loc_lng]'), loc_lat = $('input[name=loc_lat]');
    locator.change(() => {
        loc_lng.val(locator.lng());
        loc_lat.val(locator.lat());
        $('.locator-addr').text(locator.address()).removeAttr('hidden');
    });
    locator.create();
    $('#locator-show-cr').click(() => locator.render($('#create-shop-modal input[name=addr]').val()));
    $('#locator-show-ch').click(() => locator.render($('#change-shop-modal input[name=addr]').val()));
    $('#change-dish-commit').click(change_dish_info);
    $('#change-dish-modal').on('show.bs.modal', (evt) => {
        $('#change-dish-id')
            .val($(evt.relatedTarget).attr('dish-id'))
            .attr('shop-id', $(evt.relatedTarget).attr('shop-id'));
    });
    $('#create-dish-commit').click(create_dish);
    $('#create-dish-modal').on('show.bs.modal', (evt) => {
        $('#create-dish-shop-id')
            .val($(evt.relatedTarget).attr('shop-id'));
    });
    $('#change-shop-commit').click(change_shop_info);
    $('#change-shop-modal').on('show.bs.modal',
        (evt) => $('#change-shop-id').val($(evt.relatedTarget).attr('shop-id')));
    $('#create-shop-commit').click(create_shop);
    $('#finish-order-commit').click(finish_order_commit);
    $('#finish-order-modal').on('show.bs.modal', (evt) => {
        $('#finish-order-commit')
            .attr('order-id', $(evt.relatedTarget).attr('order-id'))
            .attr('shop-id', $(evt.relatedTarget).parent().parent().parent().attr('id').split('-')[2]);
    });
    $('#logout').click(
        () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
});
