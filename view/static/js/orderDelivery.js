function orderDelivery(order_id){
    var data = {"order_id": order_id};
    $.ajax({
        url: "/order/finish",
        type: "POST",
        data: data, 
        success: function(data){
            window.location.href = "/index.html";
        }
    });
}

$(document).load(function(){
    $("#order-delivery").click(set-order-delivery);
});