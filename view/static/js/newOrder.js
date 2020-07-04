function newOrder(shop_id, dish_id, amount, addr, loc_lng, loc_lat, remarks){
    var data = {
        "shop_id": shop_id, 
        "dish_id": dish_id, 
        "amount": amount,
        "addr": addr,
        "loc_lng": loc_lng,
        "loc_lag": loc_lat,
        "remarks": remarks
    };
    $.ajax({
        url: "/order/new",
        type: "POST",
        data: data,
        succcess: function(data){
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
    $("#").click(newOrder); //TODO
});  