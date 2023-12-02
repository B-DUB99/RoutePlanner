var markers = new Map();
var lines = [];
var markerLayer = L.layerGroup();
var layers = [];
let dest;
let pathArray;
let directions;

const redIcon = new L.Icon({
    iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
	shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

const greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

function createMarker(event) {
	if (event.latlng.lat >= 42.157 && event.latlng.lat <= 42.369062 && event.latlng.lng >= -85.6995747 && event.latlng.lng <= -85.531 && markers.size != 2) {
        // used to place marker on top of map
        if (markers.size < 2) {
			let marker;
			if (markers.size == 0){
                marker = L.marker(event.latlng, {
               	    draggable: true,
                    icon: greenIcon,
                    title: 'Start'
           	    });
			}else if(markers.size == 1){
                marker = L.marker(event.latlng, {
                    draggable: true,
                    icon: redIcon,
                    title: 'Destination'
                });
            }

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
		alert("Error! \nEither both markers are placed \nor you clicked out of bounds.");
	}
}

async function passToFlask() {
    let chosenTransport = Array.from(document.getElementsByName('transport')).find(ele => ele.checked).value;
    const response = await fetch(`/${JSON.stringify([markers.get(1), markers.get(2), myRange.value, chosenTransport])}`, {
        method: 'POST',
        body: JSON.stringify([markers.get(1), markers.get(2), myRange.value, chosenTransport])
    });

    data = await response.json();
    pathArray = data[0];
	directions = data[1];
	drawPathLine(pathArray);
    addDirections(directions);
}

function drawPathLine(pathArray) {
    for (let i = 0; i < pathArray.length - 1; i++) {
        var line = new L.Polyline([pathArray[i], pathArray[i + 1]], {
            color: 'red',
            weight: 5,
            opacity: 0.75,
            smoothFactor: 1
        });
        lines[i] = line;
        line.addTo(markerLayer);
    }
}

function addDirections(directions) {
    dirSidebar = document.querySelector('.direction-sidebar');
    dirSidebar.style.width = '350px';

    for (var i = 0, totDist = 0; i < directions.length; i++) {
        totDist += directions[i][2];
        dirTag = document.createElement('p')
        dirTag.innerHTML = directions[i][0].slice(0, 8) + directions[i][2].toString() + ' meters ' + directions[i][0].slice(8, directions[i][0].length);
        dirSidebar.appendChild(dirTag)
    }

    distTag = document.createElement('p')
    distTag.innerHTML = 'Total Distance: ' + totDist.toString() + ' meters'
    dirSidebar.appendChild(distTag)
}

function hideDirections() {
    document.querySelector('.direction-sidebar').style.width = '0px';
    document.querySelectorAll('.direction-sidebar > *').forEach(item => item.remove())
}

// adjust this so that on mouse hover popup procs or opacity changes
function createAmenMarkers(amens, id) {
	var amenMarkerLayer = L.layerGroup();
    var chosenIcon;
    if (id == "Grocery") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Grocery_XL_round_icon.png"});
    else if (id == "Businesses") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Business_XL_round_icon.png"});
    else if (id == "Community_Hubs") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Community_Hub_XL_round_icon.png"});
    else if (id == "Bike_Shops") chosenIcon =  L.icon({iconUrl: "static/images/GPS_Icons/GPS_Bike_Shop_XL_round_icon.png"});
    else if (id == "Bike_Parking") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_bike_XL_round_icon.png"});
    else if (id == "Worlds_of_Wonder") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_WoW_XL_round_icon.png"});
    else if (id == "Pharmacy") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Health_and_Wellness_XL_round_icon.png"});
    else if (id == "Books") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Book_XL_round_icon.png"});
    else if (id == "Cafe") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Cafe_XL_round_icon.png"});
    else if (id == "Drink") chosenIcon = L.icon({ iconUrl: "static/images/GPS_Icons/GPS_Drink_XL_round_icon.png"});
    else if (id == "Food") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Resturants_XL_round_icon.png"});
    else if (id == "Treats") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Ice_Cream_XL_round_icon.png"});
    else if (id == "Bathrooms,_Drinking_Fountains") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Restroom_XL_round_icon.png"});
    else if (id == "Bike_Repair") chosenIcon = L.icon({iconUrl: "static/images/GPS_Icons/GPS_Bike_Shop_and_Repair_XL_round_icon.png"});
    else if (id == "Art") chosenIcon = L.icon({ iconUrl: "static/images/GPS_Icons/GPS_Art_XL_round_icon.png"});
    else if (id == "Sculptures") chosenIcon = L.icon({ iconUrl: "static/images/GPS_Icons/GPS_WoW_XL_round_icon.png"});
	for(let i = 0; i < amens.length; i++){
		var latlng = L.latLng(amens[i][0]["lat"], amens[i][0]["lon"]);
		let marker = L.marker(latlng, {
            icon: chosenIcon,
			title: amens[i][0]["name"],
		}).on('click', (e) => {
            dest = e.latlng;
        });
		marker.addTo(amenMarkerLayer).bindPopup(amens[i][0]["name"] + "<br>" + amens[i][0]["desc"] + "<br><img src=\"" + amens[i][0]["pic_loc"] + "\" width = 300><div style='text-align:center'><button onclick='setDest();'>Here</button></div>", {
            offset: [11, 5]
        });
    }
	amenMarkerLayer.id = id
	layers.push(amenMarkerLayer)
    amenMarkerLayer.addTo(map);
}

function setDest() {
    if (markers.size == 0) {
        let marker = L.marker(dest, {
            draggable: true,
            icon: greenIcon 
        });
        marker.id = 1;
        markers.set(1, marker._latlng);
        marker.on("click", deleteMarker);
        marker.on("dragend", newCoords);
        marker.addTo(markerLayer);
        markerLayer.addTo(map);
    }else if(markers.size == 1){
        let marker = L.marker(dest, {
            draggable: true,
            icon: redIcon
        });
        marker.id = 2;
        markers.set(2, marker._latlng);
        marker.on("click", deleteMarker);
        marker.on("dragend", newCoords);
        marker.addTo(markerLayer);
        markerLayer.addTo(map);
    }else if(markers.size == 2){
        markers[1].remove()
        let marker = L.marker(dest, {
            draggable: true,
            icon: redIcon
        });
        marker.id = 2;
        markers.set(2, marker._latlng);
        marker.on("click", deleteMarker);
        marker.on("dragend", newCoords);
        marker.addTo(markerLayer);
        markerLayer.addTo(map);
    }


    if (markers.size == 2) {
        passToFlask();
    }
}

function deleteAmenMarkers(id) {
	for (let i = 0; i < layers.length; i++){
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
    hideDirections();
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
    hideDirections();
}

function newCoords() {
    removePathLine();
    markers.set(this.id, this._latlng);
    document.querySelectorAll('.direction-sidebar > *').forEach(item => item.remove())
    passToFlask();
}

map.addEventListener("click", createMarker);

