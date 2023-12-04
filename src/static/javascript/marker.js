var markers = new Map();
var lines = [];
var markerLayer = L.layerGroup();
var layers = [];
let dest;
let pathArray;
var directions = [];
let userRisk;

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
			if (markers.get(1) == undefined){
                marker = L.marker(event.latlng, {
               	    draggable: true,
                    icon: greenIcon,
                    title: 'Start'
           	    });
			} else if (markers.get(2) == undefined) {
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
		alert("Error! \nEither both markers are placed \nor you clicked out of bounds.");
	}
}

async function passToFlask() {
    addDirSidebar()
    addLoader();
	userRisk = myRange.value;
    let chosenTransport = Array.from(document.getElementsByName('transport')).find(ele => ele.checked).value;
    await fetch(`calculate_route/${JSON.stringify([markers.get(1), markers.get(2), myRange.value, chosenTransport])}`, {
        method: 'POST',
        body: JSON.stringify([markers.get(1), markers.get(2), myRange.value, chosenTransport])
    })
    .then(fetchJSON => fetchJSON.json())
    .then(pathAndDirs => {
        // call loading off directions sidebar, the load everything else
        document.querySelectorAll('.direction-sidebar > *').forEach(item => item.remove());
        
        pathArray = pathAndDirs[0];
        directions = pathAndDirs[1];

        drawPathLine(pathArray);
        addDirections(directions);
    })
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

function addDirSidebar() {
    if (mobileAndTabletCheck()) {
        dirSidebar.style.width = '100%'
        dirSidebar.style.height = '200px';
        dirSidebar.style.bottom = '0'
        document.querySelector('.leaflet-bottom.leaflet-right').style.bottom = '200px'
    } else {
        dirSidebar.style.width = '350px';
        dirSidebar.style.height = '100%'
        dirSidebar.style.right = '0'
        document.querySelector('#chngLayer').style.marginRight = '350px'
        document.querySelector('.leaflet-control-zoom').style.marginRight = '360px';
        document.querySelector('.leaflet-control-scale').style.marginRight = '360px';
    }
}

function addLoader() {
    dirTag = document.createElement('p');
    dirTag.innerHTML = 'Loading';
    dirTag.classList.add('loader');
    for (let i = 0; i < 3; i++) {
        spanTag = document.createElement('span');
        spanTag.innerHTML = '.';
        spanTag.classList.add('loader__dot');
        dirTag.append(spanTag)
    }
    dirSidebar.appendChild(dirTag);
}

function addDirections(directions) {
    addDirSidebar()
	let avgRisk = 0.0;
    let userRiskLower = 0;
	for (var i = 0, totDist = 0; i < directions.length; i++) {
        avgRisk += directions[i][1];
		totDist += directions[i][2];
        dirTag = document.createElement('p');
		dirTag.innerHTML = directions[i][0].slice(0, 8) + directions[i][2].toString() + ' meters ' + directions[i][0].slice(8, directions[i][0].length) + '<br>Path Risk Level: ' + directions[i][1].toString();
		dirTag.style.color = 'white';
        if(directions[i][1] > userRisk){
			userRiskLower = 1;
            dirTag.style.backgroundColor = 'FireBrick';
		}
		dirSidebar.appendChild(dirTag);
    }

	if(directions.length == 0){
		errTag = document.createElement('p');
		errTag.innerHTML = '<br>ERROR: could not find a path!<br><br>Please select different marker locations<br><br>';
		errTag.style.color = 'white';
		errTag.style.backgroundColor = 'FireBrick';
		dirSidebar.appendChild(errTag);
	}else{
		avgRisk = avgRisk/directions.length;
    	distTag = document.createElement('p');
    	if(userRiskLower == 1){
			distTag.innerHTML = '<br>-----------------<br>'
				+ 'Total Distance: ' + totDist.toString() + ' meters<br><br>Avg Risk: ' + avgRisk.toFixed(2).toString() 
            	+ '<br><br>Please note path returned is of higher risk than selected.';	
		}else{
			distTag.innerHTML = '<br>-----------------<br>'
				+ 'Total Distance: ' + totDist.toString() + ' meters<br><br>Avg Risk: ' + avgRisk.toFixed(2).toString();
		}
		distTag.style.color = 'white';
		dirSidebar.appendChild(distTag);
	}
}

function hideDirections() {
    // move on mobile
    if (mobileAndTabletCheck()) {
        dirSidebar.style.height = '0px';
        document.querySelector('.leaflet-bottom.leaflet-right').style.bottom = '0px'
    } else {
    // move on nonmobile
        document.querySelector('.direction-sidebar').style.width = '0px';
        document.querySelector('#chngLayer').style.marginRight = '1px'
        document.querySelector('.leaflet-control-zoom').style.marginRight = '10px';
        document.querySelector('.leaflet-control-scale').style.marginRight = '10px';
    }

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
		marker.addTo(amenMarkerLayer).bindPopup(amens[i][0]["name"] + "<br>" + amens[i][0]["desc"] + "<br><img src=\"" + amens[i][0]["pic_loc"] + "\" width = 300><div style='text-align:center'><button onclick='setDest(dest);'>Travel Here</button></div>", {
            offset: [11, 5]
        });
    }
	amenMarkerLayer.id = id
	layers.push(amenMarkerLayer)
    amenMarkerLayer.addTo(map);
}

function setDest() {
    if (markers.get(1) == undefined) {
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
    } else if (markers.get(2) == undefined) {
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

    if (markers.size == 2 && directions.length == 0) {
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
    directions = [];
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

function mobileAndTabletCheck() {
    let check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
  };

map.addEventListener("click", createMarker);
dirSidebar = document.querySelector('.direction-sidebar');
if (mobileAndTabletCheck) hideDirections();
else openNav()
