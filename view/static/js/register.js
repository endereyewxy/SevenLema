$(document).ready(function () {
    const loc_lng = $('input[name=loc_lng]'), loc_lat = $('input[name=loc_lat]');
    const locator = new Locator();
    locator.change = (lng, lat, addr) => {
        loc_lng.val(lng);
        loc_lat.val(lat);
        $('#locator-addr').text('定位到：' + addr).removeAttr('hidden');
    };
    locator.create(106.30557, 29.59899, true);
    $('#locator-show').click(() => locator.show($('input[name=addr]').val()));
    $('input[name=password]').change(function () {
        let pattern = $(this).val().replace(/([*.?+$^\[\](){}|\/\\])/g, '\\$1');
        $('#password-confirm').attr('pattern', pattern);
    });
    setLoginRegister('register');
});