var markers = new Map();
var lines = []
var markerLayer = L.layerGroup();
var amenMarkerLayer = L.layerGroup();


function createMarker(event) {
    if (event.latlng.lat >= 42.157 && event.latlng.lat <= 42.333 && event.latlng.lng >= -85.633 && event.latlng.lng <= -85.531 && markers.size != 2) {
        // used to place marker on top of map
        if (markers.size < 2) {
            let marker = L.marker(event.latlng, {
                draggable: true, 
            });
            // if statement to define the id 
            var id = (markers.get(1) == undefined) ? 1 : 2;
            marker.id = id;
            markers.set(id, marker._latlng);

            // add marker onto layer
            marker.on("click", deleteMarker);
            marker.on("dragend", newCoords);
            marker.addTo(markerLayer);
            markerLayer.addTo(map);
        }

        if (markers.size == 2) passToFlask();
        else removePathLine();
    }
}

async function passToFlask() {
    const response = await fetch(`/${JSON.stringify([markers.get(1), markers.get(2)])}`, {
        method: 'POST',
        body: JSON.stringify([markers.get(1), markers.get(2)])
    });

    const pathArray = await response.json();
    console.log(pathArray)
    drawPathLine(pathArray)
}


function drawPathLine(pathArray) {
    for (let i = 0; i < pathArray.length - 1; i++) {
        var line = new L.Polyline([pathArray[i], pathArray[i + 1]], {
            color: 'red',
            weight: 3,
            opacity: 0.5,
            smoothFactor: 1
        });
        lines[i] = line;
        line.addTo(markerLayer);
    }
}

// adjust this so that on mouse hover popup procs or opacity changes
function createAmenMarkers(amens) {
	for(let i = 0; i < amens.length; i++){
		var latlng = L.latLng(amens[i][0]["lat"], amens[i][0]["lon"]);
		let marker = L.marker(latlng, {
			title: amens[i][0]["name"]
		});
		marker.addTo(amenMarkerLayer).bindPopup(amens[i][0]["name"] + "<br>" + amens[i][0]["desc"] + "<br><img src=\"" + amens[i][0]["pic_loc"] + "\" width = 300>");
	}
    amenMarkerLayer.addTo(map);
}

function deleteAmenMarkers() {
    amenMarkerLayer.clearLayers();
    map.removeLayer(amenMarkerLayer);
}

function deleteAllMarkers() {
    markers.clear();
    lines = [];
    markerLayer.clearLayers()
    map.removeLayer(markerLayer)
}

function removePathLine() {
    for (let i = 0; i < lines.length; i++) {
        markerLayer.removeLayer(lines[i])
    }
}

function deleteMarker() {
    removePathLine();
    lines = [];
    markerLayer.removeLayer(this);
    markers.delete(this.id);
}

function newCoords() {
    removePathLine();
    markers.set(this.id, this._latlng);
    passToFlask();
}

map.addEventListener("click", createMarker);
document.getElementById("reset").addEventListener("click", deleteAllMarkers);
