const mapBox = [[42.157, -85.6995747], [42.157, -85.531], [42.369062, -85.531], [42.369062, -85.6995747], [42.157, -85.6995747]];


// Creating a map object
// center is starting location currenly WMU
var map = L.map('map', {
    center: [42.282854713740115, -85.60950279235838],
    zoom: 13, 
    minZoom: 13,
    zoomControl: false,
    maxBounds: [[42.12, -85.48], [42.4, -85.8]],
});

var polyline = L.polyline(mapBox, {color: 'red'}).addTo(map);

// scale 
L.control.scale({
    maxWidth: 150,
    position: 'bottomright'
}).addTo(map);

// add zoom button to bottom right
L.control.zoom({
    position: 'bottomright'
}).addTo(map);
        
// main layer
var osmLayer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
// bike layer
var cyclOSM = L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
	maxZoom: 20
});
// satellite
var satelliteLayer = new L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    subdomains:['mt0','mt1','mt2','mt3']
});

// change map layer
function changeLayer() {
    if (map.hasLayer(osmLayer)) {
        map.removeLayer(osmLayer);
        map.addLayer(cyclOSM);
    } else if (map.hasLayer(cyclOSM)) {
        map.removeLayer(cyclOSM);
        map.addLayer(satelliteLayer);
    } else {
        map.removeLayer(satelliteLayer);
        map.addLayer(osmLayer);
    }
}

// Adding layer to the map
map.addLayer(osmLayer);
document.getElementById("chngLayer").addEventListener("click", changeLayer);
