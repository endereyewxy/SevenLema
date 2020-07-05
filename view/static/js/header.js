let paginator, locator;

$(document).ready(() => {
    $('#user-info').popover({
        content: () => $($('#user-wrapper').html().replace('hidden', '').replace('-1', '')),
        placement: 'bottom',
        trigger: 'click',
        html: true
    });
    $('#logout').click(() =>
        $.post('/user/logout/', {csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()},
            (resp) => resp.code ? alert(resp.msg) : window.location.href = '/'));
    $('.btn-group input').parent().removeClass('active');
    $('.btn-group input:checked').parent().addClass('active');
    paginator = new Paginator('.pagination');
    locator = new Locator();
    $('#header-config-button').popover({
        content: () => $($('#serving-wrapper').html().replace('hidden', '').replace('-1', '')),
        placement: 'bottom',
        trigger: 'click',
        html: true
    });
    $('#locator-show').click(() => locator.show($('#addr').val()));
    $('#locator-addr').click(locator.show);
});


window.onscroll = function () {
    scrollFunction()
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("btn-top").style.display = "block";
    } else {
        document.getElementById("btn-top").style.display = "none";
    }
}

function moveToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}