$(document).ready(function(){

    // Initial page load
    $("header").delay(4000).fadeIn(500);
    $("#loading-panel").delay(3000).fadeOut(500);
    $("#create-panel").hide(1000).delay(3000).show(500);
    $("#simulate-panel").hide(1000);
    $("#graphs-panel").hide(1000);
    $("#settings-panel").hide(1000);


    // Navigation buttons
    function resetNav() {
        $("#button-create, #button-simulate, #button-graphs, #button-settings").removeClass("active-page");
        $("#create-panel, #simulate-panel, #graphs-panel, #settings-panel").hide(500);
    };


    // Navigation functions
    function openCreate() {
        if (!$("#button-create").hasClass("active-page")) {
            resetNav();
            $("#button-create").addClass("active-page");
            $("#create-panel").show(500);
        }
    };
    function openSimulate() {
        if (!$("#button-simulate").hasClass("active-page")) {
            resetNav();
            $("#button-simulate").addClass("active-page");
            $("#simulate-panel").show(500);
        }
    };
    function openGraphs() {
        if (!$("#button-graphs").hasClass("active-page")) {
            resetNav();
            $("#button-graphs").addClass("active-page");
            $("#graphs-panel").show(500);
        }
    };
    function openSettings() {
        if (!$("#button-settings").hasClass("active-page")) {
            resetNav();
            $("#button-settings").addClass("active-page");
            $("#settings-panel").show(500);
        }
    };
    
    // Navigation button click events
    $("#button-create").click(function() {
        openCreate();
    });
    $("#button-simulate").click(function() {
        openSimulate();
    });
    $("#button-graphs").click(function() {
        openGraphs();
    });
    $("#button-settings").click(function() {
        openSettings();
    });

    // Navigation key events
    $(document).keydown(function(e) {
        switch(e.which) {
        // Right arrow key
        case 39:
            if ($("#button-create").hasClass("active-page")) {openSettings()}
            else if ($("#button-settings").hasClass("active-page")) {openSimulate()}
            else if ($("#button-simulate").hasClass("active-page")) {openGraphs()};
            break;
        // Left arrow key
        case 37:
            if ($("#button-graphs").hasClass("active-page")) {openSimulate()}
            else if ($("#button-simulate").hasClass("active-page")) {openSettings()}
            else if ($("#button-settings").hasClass("active-page")) {openCreate()}
            break;
        };
      });


});
