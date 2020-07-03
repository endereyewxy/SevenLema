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
        this.container = container;
        this._create_html();
    }

    change() {
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
        this.html += this.next;
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
                    object._max_pages++;
                    object.change();
                }
            } else {
                object._curr_page = Number(tag);
                object.change();
            }
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
