app.initialize = function() {
    app.view = new app.AppView();
}



app.initialize();


// don't leave out django's csrf token on ajax requests
$(function() {
    var tokenValue = $('meta[name="csrf-token"]').attr('content');

    $.ajaxSetup({
        headers: {'X-CSRFToken': tokenValue }
    })
});
