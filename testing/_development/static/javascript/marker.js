var markers = new Map();

function createMarker(event) {
    if (markers.size < 2) {
        let marker = L.marker(event.latlng, {
            draggable: true
        });
        marker.id = markers.size + 1;
        markers.set(markers.size + 1, marker._latlng);
        marker.on("click", deleteMarker);
        marker.on("dragend", newCoords);
        marker.addTo(map);
    }
    if (markers.size == 2){
        // markers.get(1).lat
        var firstpolyline = new L.Polyline([markers.get(1), markers.get(2)], {
            color: 'red',
            weight: 3,
            opacity: 0.5,
            smoothFactor: 1
        });
        firstpolyline.addTo(map);
    }
}

function deleteMarker() {
    map.removeLayer(this);
    markers.delete(this.id);
}

function newCoords() {
    markers.set(this.id, this._latlng);
}

map.addEventListener("click", createMarker);