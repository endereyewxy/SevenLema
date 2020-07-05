function setLoginRegister(method) {
    const form = $('form');
    $('#' + method).click(() => {
        form.addClass('was-validated');
        !$('input:invalid').length && $.post('/user/' + method + '/', form.serializeArray(),
            resp => resp.msg ? $('#err-msg').text(resp.msg).removeAttr('hidden') : window.location.href = "/");
    })
}