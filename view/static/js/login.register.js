function setLoginRegister(method) {
    const form = $('form'), button = $('#' + method);
    button.click(() => {
        form.addClass('was-validated');
        if (!$('input:invalid').length) {
            miscellaneous.loadingButton(button);
            miscellaneous.web.post('/user/' + method + '/', form.serializeArray(),
                () => window.location.href = "/",
                () => miscellaneous.loadingButton(button));
        }
    });
}