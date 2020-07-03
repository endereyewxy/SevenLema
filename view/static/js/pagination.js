function createPages(curr, page, callback) {
    const prev = "<li class=\"page-item\">" +
        "           <a class=\"page-link\" href=\"#\" aria-label=\"prev\">" +
        "               <span aria-hidden=\"true\">&laquo;</span>" +
        "           </a>" +
        "         </li>";
    const next = "<li class=\"page-item\">" +
        "           <a class=\"page-link\" href=\"#\" aria-label=\"next\">" +
        "               <span aria-hidden=\"true\">&raquo;</span>" +
        "           </a>" +
        "         </li>";

    function addHtml(l, r) {
        for (let i = l; i <= r; i++) {
            html += "<li class=\"page-item" +
                (i === curr ? " active" : "") +
                "\"><a class=\"page-link\" href=\"#\" aria-label=\"" + i + "\">" + i + "</a></li>";
        }
    }

    function addDots() {
        html += "<li class=\"page-item disabled\"><a class=\"page-link\" href=\"#\">...</a></li>";
    }

    let html = prev;
    if (page <= 10) {
        addHtml(1, page);
    } else if (curr <= 5) {
        addHtml(1, 7);
        addDots();
    } else {
        addHtml(1, 2);
        addDots();
        addHtml(curr - 2, Math.min(curr + 2, page));
        if (curr + 2 < page) {
            addDots();
        }
    }
    html += next;
    $('.pagination').html(html);
    $('.page-link').click(function () {
        let tag = $(this).attr('aria-label');
        if (tag === 'prev') {
            if (curr > 1) {
                callback(curr - 1);
            }
        } else if (tag === 'next') {
            if (curr < page) {
                callback(curr + 1);
            }
        } else {
            callback(Number(tag));
        }
    });
}
