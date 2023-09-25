var markers = new Map();
var lines = []

function createMarker(event) {

    if (markers.size < 2) {
        let marker = L.marker(event.latlng, {
            draggable: true, 
            icon: L.divIcon({
                html: "<span style='background-color:none;width: 3rem;height: 3rem;display: block;left: -1.25rem;top: -3.25rem;position: relative;border-radius: 3rem 3rem 0; transform: rotate(45deg); border:1px solid;' />"
            })
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
    if (markers.size == 2) {
        // take markers map and create a list of the two lat/long to be sent to python
        let marks = [markers.get(1), markers.get(2)];
        const req = new XMLHttpRequest();
        req.open("POST", `/${JSON.stringify(marks)}`);
        req.send();
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
    }``
}

function changeAmenMarkers(event) {

	var post_info = [event.target.id];
    const request = new XMLHttpRequest();

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var amens = JSON.parse(this.responseText);
            console.log(amens);
            if(event.target.checked){
                for(let i = 0; i < amens.length; i++){
 		      		var latlng = L.latLng(amens[i][0]["lat"], amens[i][0]["lon"]);
        			let marker = L.marker(latlng, {
            						title: amens[i][0]["name"]
        			});
					marker.id = event.target.id;
        			marker.addTo(map).bindPopup(amens[i][0]["name"] + "<br>" +
         			amens[i][0]["desc"] + "<br><img src=\"" + amens[i][0]["pic_loc"] + "\" width = 300>");
				}
            }else{
                deleteAllMarkers();
            }
        }
    };                                                                                 
	request.open("POST", `/calculate/${JSON.stringify(post_info)}`);
    request.send();
}

function draw_line(from, to, color, thickness) {
    var line = new L.Polyline([from, to], {
        color: color,
        weight: thickness,
        opacity: 1,
        smoothFactor: 1
    });
    line.addTo(map);
}

function deleteAllMarkers() {
    let icons = document.getElementsByClassName("leaflet-marker-icon");
    let shadows = document.getElementsByClassName("leaflet-marker-shadow");
    // delete markings from map
    while (icons.length > 0) {
        icons[0].remove();
        shadows[0].remove();
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
    map.removeLayer(lines[0]);
    if (markers.size == 2){
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


map.addEventListener("click", createMarker);
var elements = document.getElementsByClassName("amen-choice")
for (let i = 0; i < elements.length; i++){
	elements[i].addEventListener("change", changeAmenMarkers);
}
document.getElementById("reset").addEventListener("click", deleteAllMarkers);
