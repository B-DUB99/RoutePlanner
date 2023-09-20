
// js for slider
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");

// dom for sidebar
var sidebar = document.getElementById("mySidenav");
var main = document.getElementById("main");
var openNavBtn = document.getElementById("openNav");

// dom for about and help popups
var helpPopUp = document.getElementById("help_content");
var aboutPopUp = document.getElementById("about_content");
var fadeBackground = document.getElementById("fade");
var closeBtn = document.getElementsByClassName("closePopUp");
var openBtn = document.getElementsByClassName("white_content");

output.innerHTML = slider.value; // Display the default slider value

var dropdown = document.getElementsByClassName("dropdown-btn");

// js for sidebar
function openNav() {
    sidebar.style.width = "275px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
    main.style.opacity = 0;
    openNavBtn.style.cursor = "default";
}

function closeNav() {
    sidebar.style.width = "0";
    main.style.marginLeft= "0";
    document.body.style.backgroundColor = "white";
    main.style.opacity = 1;
    openNavBtn.style.cursor = "pointer";
}

for (var i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "flex") {
            dropdownContent.style.display = "none";
        } else {
            dropdownContent.style.display = "flex";
            dropdownContent.style.flexDirection = "column";
        }
    });
}

// used to open and close help and about tabs
function open() {
    if (this.id == "help") {
        helpPopUp.style.display = "grid";
        helpPopUp.style.opacity = .6;
    } else if (this.id == "about") {
        aboutPopUp.style.display = "grid";
        aboutPopUp.style.opacity = .6;
    }
    fadeBackground.style.display = "grid"; 
    fadeBackground.style.opacity = .8;
    sidebar.style.opacity = 0;
    sidebar.style.transition = "0s";
}

function close() {
    if (helpPopUp.style.display == "grid") {
        helpPopUp.style.display = "none";
    } else {
        aboutPopUp.style.display = "none";
    }
    fadeBackground.style.display = "none";
    sidebar.style.opacity = .8;
    sidebar.style.transition = "0.5s";
}

// used to get all input options for the route
function get_input() {
    // get transport type
    var transport = document.getElementsByName("transport");
    var transport_type = "";
    for(i = 0; i < transport.length; i++){
        if(transport[i]["checked"]){
            transport_type = transport[i]["value"];
            break;
        }
    }
    // get road type info
    var road = document.querySelectorAll("#road_type_list li");
    var road_info = [];
    for(i = 0; i < road.length; i++){
        road_info[i] = road[i]["childNodes"][3]["value"];
    }
    // get amenities
    var amen = document.getElementsByClassName("amen-choice");
    var amenities = [];
    for(i = 0; i < amen.length; i++){
        if(amen[i]["childNodes"][1]["checked"]){
            amenities.push(amen[i]["childNodes"][1]["name"]);
        }
    }
    // send to python
    // transport type will be a string ("" if none were selected)
    // road types will be a list [speed, car avoidance, bike lane preference, sidewalk preference]
    // amenities will be a list of names ([] if none were selected)
    var post_info = [transport_type, road_info, amenities];
    const request = new XMLHttpRequest();

	request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
			var amens = JSON.parse(this.responseText);
			console.log(amens);
			if(amens.length > 0){
				createAmenMarkers(amens);
			}else{
				deleteAllMarkers();
			}
		}
    };
    request.open("POST", `/calculate/${JSON.stringify(post_info)}`);
    request.send();

}


// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
}

// dom for eventlisteners
document.getElementById("openNav").addEventListener("click", openNav);
document.getElementById("closeNav").addEventListener("click", closeNav);
document.getElementById("help").addEventListener("click", open);
document.getElementById("about").addEventListener("click", open);
document.getElementById("calculate").addEventListener("click", get_input);
for (i = 0; i < openBtn.length; i++) {
    openBtn[i].addEventListener("click", close);
}
for (i = 0; i < closeBtn.length; i++) {
    closeBtn[i].addEventListener("click", close);
}
