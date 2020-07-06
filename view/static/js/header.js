const get_order = () => $('.btn-group input:checked').attr('id');

$(document).ready(() => {
    $('#user-info').popover({
        content: () => $($('#user-wrapper').html().replace('hidden', '').replace('-1', '')),
        placement: 'bottom',
        trigger: 'click',
        html: true
    });
    $('#header-config-button').popover({
        content: () => $($('#serving-wrapper').html().replaceAll('-1', '')),
        placement: 'bottom',
        trigger: 'click',
        html: true
    });
    $('#logout').click(
        () => miscellaneous.web.post('/user/logout/', {}, () => window.location.href = '/'));
    $('#locator-show').click(() => locator.render($('#addr').val()));
    $('#locator-addr').click(locator.render);
});


window.onscroll = () => document.getElementById("btn-top").style.display =
    (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) ? 'block' : 'none';
