function viewOrders(order_id, shop_id, page, limit){
    var data = {
        order_id: "order_id",
        shop_id: "shop_id",
        page: "page",
        limit: "limit",
        unfinished: "unfinished"
    };

    $.ajax({
        url = "/order/info",
        type = "GET",
        data: data,
        success: function(data){
            if(data.msg === 0){
                $("#").tmpl(data.data).appendTo("#"); //TODO
            }
            else{
                $('#alert').text(data.msg).removeAttr('hidden');
            }

        }
    });
}

$(document).load(function(){
    $("#").click(viewOrders); //TODO
});  