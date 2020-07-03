function login(username,password,addr,loc_lng,loc_lat,phone){
    var data{
        "username" : username,
        "password" : password,
        "addr" : addr,
        "loc_lng" : loc_lng,
        "loc_lat" : loc_lat,
        "phone" : phone
    };
    $.ajax({
        url:"/user/register",
        data:data,
        type:"post",
        success:function(data){
            if(data.msg === 0){
                window.location.href ="/index.html";
            }
            else{
                alert(data.msg);
            }
        }
    });
}

$(document).load(function () {
    $('#register').click(register);
});