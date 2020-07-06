$(document).ready(function () {
    const loc_lng = $('input[name=loc_lng]'), loc_lat = $('input[name=loc_lat]');
    locator.change(() => {
        loc_lng.val(locator.lng());
        loc_lat.val(locator.lat());
        $('#locator-addr').text('定位到：' + locator.address()).removeAttr('hidden');
    });
    locator.create();
    $('#locator-show').click(() => locator.render($('input[name=addr]').val()));
    $('input[name=password]').change(function () {
        let pattern = $(this).val().replace(/([*.?+$^\[\](){}|\/\\])/g, '\\$1');
        $('#password-confirm').attr('pattern', pattern);
    });
    setLoginRegister('register');
});