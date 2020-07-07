(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.miscellaneous = factory();
    }
}(this, function () {
    const alert = (msg) => {
        let container = $('#alert-container');
        if (!container.length) {
            container = $('<div id="alert-container" style="position: fixed;top: 10px;right: 10px"></div>')
                .appendTo($('body'));
        }
        const target = $(
            `<div class="alert alert-danger alert-dismissible" role="alert">
                <strong>${msg}</strong>
                <a type="button" class="close" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </a>
            </div>`
        );
        target.children('a').click(() => animate(target, 'fadeOutLeft', () => target.remove()));
        animate(target, 'fadeInUp');
        target.appendTo(container);
    };

    const popover = (container, content) => container.popover({
        html: true,
        content: () => $(content.html().replace(/-1/g, '')),
        placement: 'bottom',
        trigger: 'click',
    });

    const loading_button = (target) => {
        let sr = target.children('.sr-only');
        target.html(sr.length
            ? sr.html()
            : `<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
               <span class="sr-only">${target.html()}</span>`);
        sr.length ? target.removeAttr('disabled') : target.attr('disabled', 'disabled');
    };

    const animate = (target, effect, finished) => {
        const classes = `animate__animated animate__${effect}`;
        target.addClass(classes)[0].addEventListener('animationend', () => {
            target.removeClass(classes);
            finished && finished(target);
        });
        return target;
    };

    const load_template = (container, template, data, keep = false) => {
        if (!data.length) {
            return;
        }
        !keep && container.html('');
        animate(template.tmpl(data), 'fadeInUp').each(
            (i, item) => setTimeout(() => container.append(item), 100 * i));
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
        alert: alert,
        popover: popover,
        animate: animate,
        loadingButton: loading_button,
        loadTemplate: load_template,
        web: {
            get: web_get,
            post: web_post
        }
    }
}));
