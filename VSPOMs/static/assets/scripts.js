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
    }
    // Show create page
    $("#button-create").click(function(){
        if (!$(this).hasClass("active-page")) {
            resetNav(); $("#button-create").addClass("active-page"); $("#create-panel").show(500);
        }
    });
    // Show simulate page
    $("#button-simulate").click(function(){
        if (!$(this).hasClass("active-page")) {
            resetNav(); $("#button-simulate").addClass("active-page"); $("#simulate-panel").show(500);
        }
    });
    // Show graphs page
    $("#button-graphs").click(function(){
        if (!$(this).hasClass("active-page")) {
            resetNav(); $("#button-graphs").addClass("active-page"); $("#graphs-panel").show(500);
        }
    });
    // Show settings page
    $("#button-settings").click(function(){
        if (!$(this).hasClass("active-page")) {
            resetNav(); $("#button-settings").addClass("active-page"); $("#settings-panel").show(500);
        }
    });

});
