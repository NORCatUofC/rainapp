var nyearTable = {};
function setupNYearTable(nyearTableArg) {
    nyearTable = nyearTableArg;
    drawNYearTable(100);
}

function drawNYearTable(n, drawFull) {
    $("#nyearTable").empty();
    $("#placeForPaginationBtn").empty();
    var events = nyearTable[n];
    var tableStr = "";
    var numToShow = events.length;
    const MAX_TO_SHOW = 7;
    $("#nYearStormSelected").text(n);
    if (events.length > MAX_TO_SHOW) {
        if (drawFull) {
            var r = $('<button type="button" style="text-align:center" class="btn btn-primary" onclick="drawTableAndMoveUp(' + n + ', false)">See Less</button>');
            $("#placeForPaginationBtn").append(r);
        }
        else {
            numToShow = MAX_TO_SHOW;
            var r = $('<button type="button" style="text-align:center" class="btn btn-primary" onclick="drawNYearTable(' + n + ', true)">See More</button>');
            $("#placeForPaginationBtn").append(r);
        }
    }
    for (var i = 0; i < numToShow; i++) {
        var event = events[i];
        tableStr += "<tr><td>" + event.date_formatted + "</td>" +
            "<td>" + event.inches + " inches in " + event.duration_formatted + "</td>" +
            "<td><a href='" + event.event_url + "' class='btn btn-primary btn-xs'>See it</a></td></tr>"
    }
    $('#nyearTable').append(tableStr);

}

function drawTableAndMoveUp(n, drawFull) {
    drawNYearTable(n, drawFull);
    $("body, html").scrollTop($("#nYearStormSelected").offset().top);
}