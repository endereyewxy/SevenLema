function sort_mode(shop_id,name,order,page,limit,serving){
    var data = {
        "shop_id":shop_id,
        "name" : $('#header-search').value(),
        "order" : order,
        "page" : page,
        "limit" : limit,
        "serving" : serving
    }
    $.ajax({
        url:"/search/shop",
        data:data,
        type:"get",
        success:function(data){
            var num = data.page;    //todo
            //这里是数据
            var userLangs = data.data;
            //模板   绑定    数据      添加到   指定的div或者是容器里面
            $('#each').tmpl(userLangs).appendTo('#eachList');
        }
    });
}
$(document).load(function () {
    $('#header-search-button').click(sort_mode);
    $('#sme-name').click(sort_mode);    //order_id
});
