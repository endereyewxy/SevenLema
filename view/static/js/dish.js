let paginator, locator, card_list = [], serving = false;

function amount_change(dish_id) {
    const input = $("#dish-" + dish_id);
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
        if ((changed_amount % 1) !== 0) {
            changed_amount = changed_amount.toFixed(0);
        }
        for (let i = 0; i < card_list.length; i++) {
            if (dish_id === card_list[i].dish_id) {
                card_list[i].amount = changed_amount;
                break;
            }
        }
    }
    calc_total_price();
    input.val(changed_amount);

}

function add_dish_to_card(name, dish_id, image, price) {
    let flag = false;
    for (let i = 0; i < card_list.length; i++) {
        if (card_list[i].dish_id === dish_id) {
            card_list[i].amount++;
            flag = true;
            break;
        }
    }
    if (!flag) {
        card_list = card_list.concat([{
            name: name,
            dish_id: dish_id,
            image: image,
            price: price,
            amount: 1
        }]);
    }
    calc_total_price();
    $('#card-list-container').html($('#card-list-template').tmpl(card_list));

}

function calc_total_price() {
    let sum = 0;
    for (let i = 0; i < card_list.length; i++) {
        sum += card_list[i].price * card_list[i].amount;
    }
    $('#total-price').val("总价：￥" + sum.toFixed(2));
}


function get_order() {
    return $('label.active input').attr('id');
}

function load_dish() {
    const data = {
        shop_id: shop_id,
        name: $('#header-search').val(),
        order: get_order(),
        page: paginator.currPage,
        limit: 5,
        serving: serving
    };
    $.ajax({
        url: '/search/dish',
        data: data,
        type: 'get',
        success: function (resp) {
            paginator.maxPages = resp.page;
            $('#data-container').html($('#data-template').tmpl(resp.data));
        }
    });
}

$(document).ready(function () {
    // Create and configure paginator
    paginator = new Paginator('.pagination');
    paginator.change = load_dish;

    // Create and configure locator
    locator = new Locator();
    locator.change = function (lng, lat, addr) {
        $('#locator-addr').text(addr);
    };
    if (default_lng !== undefined) {
        locator.create(default_lng, default_lat);
    } else {
        locator.create(106.30557, 29.59899, true);
    }
    $('#header-config-button').popover({
        content: $('#serving-wrapper'),
        placement: 'bottom',
        trigger: 'click',
        html: true
    });
    $('#locator-show').click(function () {
        locator.show($('#addr').val());
    });
    $('#locator-addr').click(locator.show);

    // Bind loading functions
    $('#header-search-button,#price,#sales').click(load_dish);

    // Initialize settings
    load_dish();
});