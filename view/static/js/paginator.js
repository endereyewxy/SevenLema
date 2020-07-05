class Paginator {
    constructor(container) {
        this.prev = "<li class=\"page-item\">" +
            "           <a class=\"page-link\" href=\"#\" aria-label=\"prev\">" +
            "               <span aria-hidden=\"true\">&laquo;</span>" +
            "           </a>" +
            "        </li>";
        this.next = "<li class=\"page-item\">" +
            "            <a class=\"page-link\" href=\"#\" aria-label=\"next\">" +
            "                <span aria-hidden=\"true\">&raquo;</span>" +
            "            </a>" +
            "        </li>";
        this._curr_page = 1;
        this._max_pages = 1;
        this.limit = 5;
        this.container = container;
        this._create_html();

        this._create_html = this._create_html.bind(this);
        this._add_page = this._add_page.bind(this);
        this._add_dots = this._add_dots.bind(this);
    }

    get currPage() {
        return this._curr_page;
    }

    set currPage(currPage) {
        this._curr_page = currPage;
        this._create_html();
    }

    get maxPages() {
        return this._max_pages;
    }

    set maxPages(maxPages) {
        this._max_pages = maxPages;
        if (this._curr_page > this._max_pages)
            this._curr_page = this._max_pages;
        this._create_html();
    }

    _create_html() {
        this.html = this.prev;
        if (this._max_pages <= 10) {
            this._add_page(1, this._max_pages);
        } else if (this._curr_page <= 5) {
            this._add_page(1, 7);
            this._add_dots();
        } else {
            this._add_page(1, 2);
            this._add_dots();
            this._add_page(this._curr_page - 2, Math.min(this._curr_page + 2, this._max_pages));
            if (this._curr_page + 2 < this._max_pages) {
                this._add_dots();
            }
        }

        let selector = "<select class=\"custom-select\" style=\"width: 7rem\">" +
            "               <option " + (this.limit ===  5 ? "selected=\"selected\"" : '') + "value=\"5\">5条/页</option>" +
            "               <option " + (this.limit === 10 ? "selected=\"selected\"" : '') + "value=\"10\">10条/页</option>" +
            "               <option " + (this.limit === 20 ? "selected=\"selected\"" : '') + "value=\"20\">20条/页</option>" +
            "               <option " + (this.limit === 30 ? "selected=\"selected\"" : '') + "value=\"30\">30条/页</option>" +
            "           </select>";
        this.html += this.next + selector;
        $(this.container).html(this.html);

        const object = this;
        $('.page-link').click(function () {
            let tag = $(this).attr('aria-label');
            if (tag === 'prev') {
                if (object._curr_page > 1) {
                    object._curr_page--;
                    object.change();
                }
            } else if (tag === 'next') {
                if (object._curr_page < object._max_pages) {
                    object._curr_page++;
                    object.change();
                }
            } else {
                object._curr_page = Number(tag);
                object.change();
            }
        });
        $(this.container + ' select').change(function () {
            object.limit = Number($(this).val());
            object.change();
        });
    }

    _add_page(l, r) {
        for (let i = l; i <= r; i++) {
            this.html += "<li class=\"page-item" +
                (i === this._curr_page ? " active" : "") +
                "\"><a class=\"page-link\" href=\"#\" aria-label=\"" + i + "\">" + i + "</a></li>";
        }
    }

    _add_dots() {
        this.html += "<li class=\"page-item disabled\"><a class=\"page-link\" href=\"#\">...</a></li>";
    }
}
