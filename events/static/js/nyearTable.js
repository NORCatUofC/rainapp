var nyearTable = {};
function setupNYearTable(nyearTableArg) {
    nyearTable = nyearTableArg;
    drawNYearTable(100);
}

function drawNYearTable(n) {
    $("#nyearTable").empty();
    var events = nyearTable[n];
    var tableStr = ""
    for (var i = 0; i < events.length; i++) {
        var event = events[i];
        tableStr += "<tr><td>" + event.date_formatted + "</td>" +
                "<td>" + event.inches + " inches in " + event.duration_formatted + "</td>" +
                "<td><a href='" + event.event_url + "' class='btn btn-primary btn-xs'>See it</a></td></tr>"
    }
    $('#nyearTable').append(tableStr);
}