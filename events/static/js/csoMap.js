function drawCsoMap(csoMapData, csoMap) {
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'scottbeslow.1f2iop7n',
        accessToken: 'pk.eyJ1Ijoic2NvdHRiZXNsb3ciLCJhIjoiZ3J0aHNYZyJ9.J2pdf4MyW3Y-etg6Je5PXw'
    }).addTo(csoMap);

    var csoPoints = csoMapData.cso_points;

    for (var i = 0; i < csoPoints.length; i++) {
        var csoPoint = csoPoints[i];
        var marker = L.marker([csoPoint.lat, csoPoint.lon]).addTo(csoMap);
    }
}

