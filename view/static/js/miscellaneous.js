(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.miscellaneous = factory();
    }
}(this, function () {
    const popover = (container, content) => $(container).popover({
        html: true,
        content: () => $($(content).html().replace(/-1/g, '')),
        placement: 'bottom',
        trigger: 'click',
    });

    const html_loading = '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>';

    const loading_button = (selector) => {
        let target = $(selector), sr = target.children('.sr-only');
        target.html(sr.length
            ? sr.html()
            : html_loading + '<span class="sr-only">' + target.html() + '</span>');
        sr.length ? target.removeAttr('disabled') : target.attr('disabled', 'disabled');
    };

    const web_callback = (done, failed) => (resp) => {
        if (resp.code) {
            alert(resp.msg);
            failed && failed();
        } else {
            done && done();
        }
    };

    const web_get = (url, data, done, failed) => $.get(url, data, web_callback(done, failed));

    const web_post = (url, data, done, failed) => {
        data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();
        $.post(url, data, web_callback(done, failed));
    };

    return {
        popover: popover,
        loadingButton: loading_button,
        web: {
            get: web_get,
            post: web_post
        }
    }
}));
