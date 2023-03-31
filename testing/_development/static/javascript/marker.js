var markers = new Map();
var lines = []

function createMarker(event) {
    if (markers.size < 2) {
        let marker = L.marker(event.latlng, {
            draggable: true
        });
        // if statement to define the id 
        var id = (markers.get(1) == undefined) ? 1 : 2;
        marker.id = id;
        markers.set(id, marker._latlng);

        // add marker onto layer
        marker.on("click", deleteMarker);
        marker.on("dragend", newCoords);
        marker.addTo(map);
    }
    if (markers.size == 2 && lines.length == 0){
        var line = new L.Polyline([markers.get(1), markers.get(2)], {
            color: 'red',
            weight: 3,
            opacity: 0.5,
            smoothFactor: 1
        });
        lines[0] = line
        line.addTo(map);
    }
}

function deleteAllMarkers() {
    let icons = document.getElementsByClassName("leaflet-marker-icon");
    let shadows = document.getElementsByClassName("leaflet-marker-shadow");
    let line = document.getElementsByClassName("leaflet-overlay-pane");
    // delete markings from map
    while (icons.length > 0) {
        icons[0].remove();
        shadows[0].remove();
        line[0].remove();
    }
    markers.clear();
}

function deleteMarker() {
    if(markers.size == 2 || (markers.size < 2 && lines.length > 0)){
        map.removeLayer(lines[0])
        lines.pop()
    }
    map.removeLayer(this);
    markers.delete(this.id);
}

function newCoords() {
    markers.set(this.id, this._latlng);
}


map.addEventListener("click", createMarker);
document.getElementById("reset").addEventListener("click", deleteAllMarkers);