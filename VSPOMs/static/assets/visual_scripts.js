// VSPOMs Frontend Scripts, JH04 2023

$(document).ready(function(){

    // Initial page load
    $("#header-wrapper").delay(4200).fadeIn(500);
    $("#loading-panel").delay(3200).fadeOut(500);
    $("#create-panel").fadeOut(1000).delay(3000).fadeIn(500);
    $("#simulate-panel").fadeOut(1000);
    $("#graphs-panel").fadeOut(1000);
    $("#settings-panel").fadeOut(1000);
    
    // Navigation button click events
    $("#button-create").click(function() {openCreate();});
    $("#button-simulate").click(function() {openSimulate();});
    $("#button-graphs").click(function() {openGraphs();});
    $("#button-settings").click(function() {openSettings();});
    // On "Save parameters" click
    $("#button-save-parameters").click(function() {openSimulate();});
    $("#error-popup").children("button").click(function() {$("#error-popup").fadeOut(200)});
    // Open/Close Credits Page
    $("#open-credits").click(function() {$("#credits-page").fadeIn(200)});
    $("#credits-page").children("button").click(function() {$("#credits-page").fadeOut(200)});

    // Keydown events
    let p0=false;let p1=false;let p2=false;let p3=false;
    $(document).keydown(function(e) {
        switch(e.which) {
            // Right arrow key
            case 39:
                if (! $(document.activeElement).is("input")) {
                    if ($("#button-create").hasClass("active-page")) {openSettings()}
                    else if ($("#button-settings").hasClass("active-page")) {openSimulate()}
                    else if ($("#button-simulate").hasClass("active-page")) {openGraphs()};
                }
                p0=false;p1=false;p2=false;p3=false;
                break;
            // Left arrow key
            case 37:
                if (! $(document.activeElement).is("input")) {
                    if ($("#button-graphs").hasClass("active-page")) {openSimulate()}
                    else if ($("#button-simulate").hasClass("active-page")) {openSettings()}
                    else if ($("#button-settings").hasClass("active-page")) {openCreate()}
                }
                p0=false;p1=false;p2=false;p3=false;
                break;
            // Other
            case 80: p0 = true;break;
            case 65: if (p0) {p1=true;} break;
            case 82: if (p0 && p1) {p2=true;} break;
            case 84: if (p0 && p1 && p2) {p3=true} break;
            case 89:
                if (p0 && p1 && p2 && p3) {
                    $("html, body, div, header").css({
                        'background-color': 'rgb(234, 255, 0)',
                        'color': 'hotpink',
                        'font-weight': 'bold',
                        'text-transform': 'uppercase',
                        'font-family': "'Comic Sans MS', 'Comic Sans', cursive",
                        'border': '10px solid #8cff00',
                        'border-radius': '40px',
                    });
                }
                break;
            default: p0=false;p1=false;p2=false;p3=false;
        };
      });

});


// Navigation functions
function resetNav() {
    $("#button-create, #button-simulate, #button-graphs, #button-settings").removeClass("active-page");
    $("#create-panel, #simulate-panel, #graphs-panel, #settings-panel").hide(0);
};
function openCreate() {
    if (!$("#button-create").hasClass("active-page")) {
        resetNav();
        $("#button-create").addClass("active-page");
        $("#create-panel").fadeIn(200);
        $(document).prop('title', 'Create | VSPOMS');
    }
};
function openSimulate() {
    if (!$("#button-simulate").hasClass("active-page")) {
        resetNav();
        $("#button-simulate").addClass("active-page");
        $("#simulate-panel").fadeIn(200);
        $(document).prop('title', 'Simulate | VSPOMS');
    }
};
function openGraphs() {
    if (!$("#button-graphs").hasClass("active-page")) {
        resetNav();
        $("#button-graphs").addClass("active-page");
        $("#graphs-panel").fadeIn(200);
        $(document).prop('title', 'Graphs | VSPOMS');
    }
};
function openSettings() {
    if (!$("#button-settings").hasClass("active-page")) {
        resetNav();
        $("#button-settings").addClass("active-page");
        $("#settings-panel").fadeIn(200);
        $(document).prop('title', 'Parameters | VSPOMS');
    }
};

// Hide the loading frogs
function resetFrog() {
    $("#frog1").hide();
    $("#frog2").hide();
    $("#frog3").hide();
    $("#frog4").hide();
    $("#frog5").hide();
}
// Pick the frog to load
function pickFrog() {
    let frogArray = ["#frog1","#frog2","#frog3","#frog4","#frog5"];
    let chosenFrog = frogArray[Math.floor(Math.random()*frogArray.length)];
    resetFrog();
    $(chosenFrog).show();
}