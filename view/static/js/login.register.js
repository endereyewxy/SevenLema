function setLoginRegister(method) {
    const form = $('form');
    $('#' + method).click(() => {
        form.addClass('was-validated');
        if (!$('input:invalid').length) {
            miscellaneous.loadingButton('#' + method);
            miscellaneous.web.post('/user/' + method + '/', form.serializeArray(),
                () => window.location.href = "/",
                () => miscellaneous.loadingButton('#' + method));
        }
    });
}