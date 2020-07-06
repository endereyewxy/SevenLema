function setLoginRegister(method) {
    const form = $('form');
    $('#' + method).click(() => {
        form.addClass('was-validated');
        !$('input:invalid').length && miscellaneous.web.post('/user/' + method + '/', form.serializeArray(),
            resp => window.location.href = "/");
    });
}