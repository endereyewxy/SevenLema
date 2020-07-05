function load_orders() {
    const data = {
        "page": 1,
        "limit": 50
    };
    $.ajax({
        url: "/order/info",
        data: data,
        type: "get",
        success: function (data) {
            $('#info-container').html($('#info-template').tmpl(data.data));
        }
    });
}

$(document).ready(function () {
    load_orders();
});
