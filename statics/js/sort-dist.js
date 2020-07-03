/*
    container 结构如下
    <div class = "shop_container" id ="xxx">

    </div>
*/


function sort_mode(name,order,loc_lng,loc_lat,tags,page,limit,serving){
    var data = {
        "name" : name,
        "order" : "dist",
        "loc_lng" : loc_lng,
        "loc_lat" : loc_lat,
        "tags" : tags,
        "page" : page,
        "limit" : limit,
        "serving" : serving
    }
    $.ajax({
        url:"/search/shop",
        data:data,
        type:"get",
        success:function(data){
            var num=data.data.len();
        }
    });
}