let card_list = [], serving = false;

function change_dish_info() {
    let data = new FormData(document.getElementById('dish-form'));
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
        success: (resp) => resp.code ? alert(resp.msg) : ($('#dish-modal').modal('hide') & load_dish())
    });
}

function commit_an_order() {
    let dish_id_list = [], dish_amount = [];
    for (let i = 0; i < card_list.length; i++) {
        dish_id_list[i] = card_list[i].dish_id;
        dish_amount [i] = card_list[i].amount;
    }
    const data = {
        shop_id: shop_id,
        dish_id: dish_id_list,
        amount: dish_amount,
        addr: $('#addr').val(),
        loc_lng: locator.lng(),
        loc_lat: locator.lat(),
        remarks: $('#remarks').val()
    };
    miscellaneous.web.post('/order/new/', data, (resp) => window.location.href = '/');
}

function amount_change(dish_id) {
    const input = $('#dish-' + dish_id);
    let changed_amount = Number(input.val());
    if (changed_amount <= 0) {
        for (let i = 0; i < card_list.length; i++) {
            if (dish_id === card_list[i].dish_id) {
                card_list.splice(i, 1);
                $('#card-list-container').html($('#card-list-template').tmpl(card_list));
                break;
            }
        }
    } else {
        !(changed_amount % 1) && (changed_amount = Number(changed_amount.toFixed(0)));
        for (let i = 0; i < card_list.length; i++) {
            if (dish_id === card_list[i].dish_id) {
                card_list[i].amount = changed_amount;
                break;
            }
        }
    }
    !card_list.length && $('#submit-order').attr('disabled', 'disabled');
    calc_total_price();
    input.val(changed_amount);
}

function add_dish_to_card(name, dish_id, image, price) {
    let flag = false;
    if (card_list.length === 0 && $('.alert').length === 0) {
        $('#submit-order').removeAttr('disabled');
    }
    for (let i = 0; i < card_list.length; i++) {
        if (card_list[i].dish_id === dish_id) {
            card_list[i].amount++;
            flag = true;
            break;
        }
    }
    !flag && (card_list = card_list.concat([{
        name: name,
        dish_id: dish_id,
        image: image,
        price: price,
        amount: 1
    }]));
    calc_total_price();
    $('#card-list-container').html($('#card-list-template').tmpl(card_list));
}

function calc_total_price() {
    let sum = 0, amount = 0;
    for (let i = 0; i < card_list.length; i++) {
        sum += card_list[i].price * card_list[i].amount;
        amount += card_list[i].amount;
    }
    $('.badge').text(amount ? amount : '');
    $('#total-price').val('总价：￥' + sum.toFixed(2));
}

function load_dish() {
    const data = {
        shop_id: shop_id,
        name: $('#header-search').val(),
        order: get_order(),
        page: paginator.currentPage(),
        limit: paginator.limit(),
        serving: serving
    };
    miscellaneous.web.get('/search/dish/', data, (resp) => {
        paginator.maximumPage(resp.page);
        $('#data-container').html($('#data-template').tmpl(resp.data));
    });
}

$(document).ready(function () {
    $('#commit').click(commit_an_order);
    $('#dish-edit').click(change_dish_info);
    $('#dish-modal').on('show.bs.modal', (evt) => $('#dish-edit-id').val($(evt.relatedTarget).attr('id')));
    paginator.change(load_dish);
    locator.change(() => $('#locator-addr').text(locator.address()));
    default_lng !== undefined ? locator.create(default_lng, default_lat) : locator.create();
    $('#header-search-button,#price,#sales').click(load_dish);
    load_dish();
});