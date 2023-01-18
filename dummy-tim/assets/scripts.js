$(document).ready(function(){

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