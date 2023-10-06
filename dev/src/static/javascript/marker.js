var markers = new Map();
var lines = [];
var markerLayer = L.layerGroup();
var layers = [];
var grocIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Grocery_icon.png",})
var bIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Business_icon.png"});
var commIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Community_Hub_icon.png"})
var bikeRepairIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Bike_Shop_and_Reapair_icon.png"})
var bathroomIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Restroom_icon.png"})
var wellnessIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_WoW_icon.png"});


function createMarker(event) {
	if (event.latlng.lat >= 42.157 && event.latlng.lat <= 42.333 && event.latlng.lng >= -85.6995747 && event.latlng.lng <= -85.531 && markers.size != 2) {
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
 		if (markers.size == 2) {
			passToFlask(); 
		} else removePathLine();

    } else {
		//placeholder until we get something better in place
		alert("You get no marker! \nEither\n Both are placed or\nYou clicked out of bounds");
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
function createAmenMarkers(amens, id) {
	var amenMarkerLayer = L.layerGroup();
    console.log("the id is: ", id)
    var chosenIcon;
    if (id == "Grocery_Stores") chosenIcon = grocIcon;
    else if (id == "Businesses") chosenIcon = bIcon;
    else if (id == "Community_Hubs") chosenIcon = commIcon;
    else if (id == "Bike_Shops,_Repair_Stations") chosenIcon = bikeRepairIcon;
    else if (id == "Bike_Parking,_Bathrooms,_Drinking_Fountains") chosenIcon = bathroomIcon;
    else if (id == "Worlds_of_Wonder") chosenIcon = wellnessIcon;
	for(let i = 0; i < amens.length; i++){
		var latlng = L.latLng(amens[i][0]["lat"], amens[i][0]["lon"]);
        
		let marker = L.marker(latlng, {
            icon: chosenIcon,
			title: amens[i][0]["name"]
		});
		marker.addTo(amenMarkerLayer).bindPopup(amens[i][0]["name"] + "<br>" + amens[i][0]["desc"] + "<br><img src=\"" + amens[i][0]["pic_loc"] + "\" width = 300>");
	}
	amenMarkerLayer.id = id
	layers.push(amenMarkerLayer)
    amenMarkerLayer.addTo(map);
	// console.log(layers[0].id);
}

function deleteAmenMarkers(id) {
	console.log(id)
	for (let i = 0; i < layers.length; i++){
		console.log(layers[i])
		if (id === layers[i].id){
			layers[i].clearLayers();
			map.removeLayer(layers[i]);
			layers.splice(i, 1);
			break;
		}
	}
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