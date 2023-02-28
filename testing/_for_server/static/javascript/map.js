// Creating a map object
// center is starting location currenly WMU
var map = L.map('map', {
    center: [42.282854713740115, -85.60950279235838],
    zoom: 15, 
    zoomControl: false
});

// scale 
L.control.scale({
    maxWidth: 150,
    position: 'bottomright'
}).addTo(map);
        
// Creating a Layer object
var osmLayer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
// satellite
var satelliteLayer = new L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    subdomains:['mt0','mt1','mt2','mt3']
});

// change map layer
function changeLayer() {
    if (map.hasLayer(osmLayer)) {
        map.removeLayer(osmLayer);
        map.addLayer(satelliteLayer);
    } else {
        map.removeLayer(satelliteLayer);
        map.addLayer(osmLayer);
    }
}

// Adding layer to the map
map.addLayer(osmLayer);

document.getElementById("chngLayer").addEventListener("click", changeLayer);