$(document).ready(function(){

    // Initial page load
    $(".button-container").hide().delay(4000).fadeIn(500);
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
    // Show create page
    $("#button-create").click(function(){
        resetNav();
        $("#button-create").addClass("active-page"); $("#create-panel").show(500);
    });
    // Show simulate page
    $("#button-simulate").click(function(){
        resetNav();
        $("#button-simulate").addClass("active-page"); $("#simulate-panel").show(500);
    });
    // Show graphs page
    $("#button-graphs").click(function(){
        resetNav();
        $("#button-graphs").addClass("active-page"); $("#graphs-panel").show(500);
    });
    // Show settings page
    $("#button-settings").click(function(){
        resetNav();
        $("#button-settings").addClass("active-page"); $("#settings-panel").show(500);
    });

});