(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.miscellaneous = factory();
    }
}(this, function () {
    const popover = (container, content) => container.popover({
        html: true,
        content: () => $(content.html().replace(/-1/g, '')),
        placement: 'bottom',
        trigger: 'click',
    });

    const html_loading = '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>';

    const loading_button = (target) => {
        let sr = target.children('.sr-only');
        target.html(sr.length
            ? sr.html()
            : html_loading + '<span class="sr-only">' + target.html() + '</span>');
        sr.length ? target.removeAttr('disabled') : target.attr('disabled', 'disabled');
    };

    const load_template = (container, template, data, keep = false) => {
        if (!data.length) {
            return;
        }
        const rec = (i) => {
            template.tmpl(data[i]).addClass('animate__animated animate__fadeInUp').appendTo(container);
            i < data.length - 1 && new Promise((r) => setTimeout(r, 100)).then(() => rec(i + 1));
        };
        !keep && container.html('');
        rec(0);
    };

    const web_callback = (done, failed) => (resp) => {
        if (resp.code) {
            alert(resp.msg);
            failed && failed(resp);
        } else {
            done && done(resp);
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
        loadTemplate: load_template,
        web: {
            get: web_get,
            post: web_post
        }
    }
}));
