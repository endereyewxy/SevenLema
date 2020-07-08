(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.paginator = factory();
    }
}(this, function () {
    const create = (target) => {
        const html_prev =
            '<li class="page-item">' +
            '   <a class="page-link" href="#" aria-label="prev"><span aria-hidden="true">&laquo;</span></a>' +
            '</li>';
        const html_next =
            '<li class="page-item">' +
            '   <a class="page-link" href="#" aria-label="next"><span aria-hidden="true">&raquo;</span></a>' +
            '</li>';
        const html_dots = '<li class="page-item" disabled><a class="page-link" href="#">...</a></li>';
        const html_se_l = '<select class="custom-select" style="width: 7rem">';
        const html_se_r = '</select>';

        let cur_page = 1, max_page = 1, limit_ = 5, on_change = () => undefined;

        const add_page = (html, l, r) => {
            for (let i = l; i <= r; i++) {
                html +=
                    '<li class="page-item' + (i === cur_page ? ' active' : '') + '">' +
                    '   <a class="page-link" href="#" aria-label="' + i + '">' + i + '</a>' +
                    '</li>';
            }
            return html;
        };

        const update_html = () => {
            let html = html_prev;
            if (max_page <= 10) {
                html = add_page(html, 1, max_page);
            } else if (cur_page <= 5) {
                html = add_page(html, 1, 7) + html_dots;
            } else {
                html = add_page(html, 1, 2) + html_dots;
                html = add_page(html, cur_page - 2, Math.min(cur_page + 2, max_page));
                cur_page + 2 < max_page && (html += html_dots);
            }
            html += html_next + '&nbsp;' + html_se_l;
            for (let i = 5; i <= 30; i += 5) {
                html += '<option value="' + i + '"' + (i === limit_ ? ' selected' : '') + '>' + i + '条/页</option>';
            }
            html += html_se_r;
            target.html(html);
            target.find('.page-link').click(function () {
                const tag = $(this).attr('aria-label');
                if (tag === 'prev') {
                    if (cur_page === 1) {
                        return;
                    }
                    cur_page--;
                } else if (tag === 'next') {
                    if (cur_page === max_page) {
                        return;
                    }
                    cur_page++;
                } else {
                    cur_page = Number(tag);
                }
                on_change();
                update_html();
            });
            target.find('select').change(function () {
                limit_ = Number($(this).val());
                on_change();
                update_html();
            });
        };

        return {
            change: (callback) => on_change = callback,
            currentPage: (val) => val === undefined ? cur_page : update_html(cur_page = val),
            maximumPage: (val) => val === undefined ? max_page : update_html(max_page = val),
            limit: (val) => val === undefined ? limit_ : update_html(limit_ = val)
        }
    };

    return {create: create};
}));
