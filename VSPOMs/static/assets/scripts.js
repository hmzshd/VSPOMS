$(document).ready(function(){

    // Load page
    $(".button-container").hide().delay(4000).fadeIn(500);
    $("#loading-panel").delay(3000).fadeOut(500);
    $("#create-panel").hide(1000).delay(3000).show(500);
    $("#simulate-panel").hide(1000);
    $("#graphs-panel").hide(1000);
    $("#settings-panel").hide(1000);

    // Navigation buttons
    $("#button-create").click(function(){
        $("#button-create").addClass("active-page"); $("#create-panel").show(500);
        $("#button-simulate").removeClass("active-page"); $("#simulate-panel").hide(500);
        $("#button-graphs").removeClass("active-page"); $("#graphs-panel").hide(500);
        $("#button-settings").removeClass("active-page"); $("#settings-panel").hide(500);
    });
    
    $("#button-simulate").click(function(){
        $("#button-create").removeClass("active-page"); $("#create-panel").hide(500);
        $("#button-simulate").addClass("active-page"); $("#simulate-panel").show(500);
        $("#button-graphs").removeClass("active-page"); $("#graphs-panel").hide(500);
        $("#button-settings").removeClass("active-page"); $("#settings-panel").hide(500);
    });

    $("#button-graphs").click(function(){
        $("#button-create").removeClass("active-page"); $("#create-panel").hide(500);
        $("#button-simulate").removeClass("active-page"); $("#simulate-panel").hide(500);
        $("#button-graphs").addClass("active-page"); $("#graphs-panel").show(500);
        $("#button-settings").removeClass("active-page"); $("#settings-panel").hide(500);
    });

    $("#button-settings").click(function(){
        $("#button-create").removeClass("active-page"); $("#create-panel").hide(500);
        $("#button-simulate").removeClass("active-page"); $("#simulate-panel").hide(500);
        $("#button-graphs").removeClass("active-page"); $("#graphs-panel").hide(500);
        $("#button-settings").addClass("active-page"); $("#settings-panel").show(500);
    });

});