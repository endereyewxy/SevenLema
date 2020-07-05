$(document).ready(function() {
    $('#user-info').popover({
        content: () => $($('#user-wrapper').html().replace('hidden', '').replace('-1', '')),
        placement: 'bottom',
        trigger: 'click',
        html: true
    });
});