const get_order = () => $('.btn-group input:checked').attr('id');

$(document).ready(() => {
    miscellaneous.popover($('#user-info'), $('#user-wrapper'));
    miscellaneous.popover($('#header-config-button'), $('#serving-wrapper'));
    $('#logout').click(
        () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
    $('#locator-show').click(() => locator.render($('#addr').val()));
    $('#locator-addr').click(locator.render);
});


window.onscroll = () => document.getElementById("btn-top").style.display =
    (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) ? 'block' : 'none';