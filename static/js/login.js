function login(username,password){
    const data{
        "username" : username,
        "password" : password
    };
    $.ajax({
        url:"/user/login",
        data:data,
        type:"post",
        success:function(data){
            if(data.code === 0){
                window.location.href ="/index.html";
            }
            else{
                alert(data.msg);
            }
        }
    });
}

$(document).load(function () {
    $('#login').click(login);
});