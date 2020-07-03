function login(){
    $.ajax({
        url:"/user/logout",
        data:data,
        type:"post",
        success:function(data){
                window.location.href ="/index.html";
        }
    });
}

$(document).load(function () {
    $('#logout').click(logout);
});