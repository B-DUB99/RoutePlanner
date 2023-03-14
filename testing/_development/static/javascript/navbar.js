
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


// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
}

// dom for eventlisteners
document.getElementById("openNav").addEventListener("click", openNav);
document.getElementById("closeNav").addEventListener("click", closeNav);
document.getElementById("help").addEventListener("click", open);
document.getElementById("about").addEventListener("click", open);
for (i = 0; i < openBtn.length; i++) {
    openBtn[i].addEventListener("click", close);
}
for (i = 0; i < closeBtn.length; i++) {
    closeBtn[i].addEventListener("click", close);
}