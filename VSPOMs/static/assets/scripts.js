// VSPOMs Frontend Scripts, JH04 2023

$(document).ready(function(){

    // Initial page load
    $("#header-wrapper").delay(4000).fadeIn(500);
    $("#loading-panel").delay(3000).fadeOut(500);
    $("#create-panel").fadeOut(1000).delay(3000).fadeIn(500);
    $("#simulate-panel").fadeOut(1000);
    $("#graphs-panel").fadeOut(1000);
    $("#settings-panel").fadeOut(1000);


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
        }
    };

    function openSimulate() {
        if (!$("#button-simulate").hasClass("active-page")) {
            resetNav();
            $("#button-simulate").addClass("active-page");
            $("#simulate-panel").fadeIn(200);
        }
    };

    function openGraphs() {
        if (!$("#button-graphs").hasClass("active-page")) {
            resetNav();
            $("#button-graphs").addClass("active-page");
            $("#graphs-panel").fadeIn(200);
        }
    };

    function openSettings() {
        if (!$("#button-settings").hasClass("active-page")) {
            resetNav();
            $("#button-settings").addClass("active-page");
            $("#settings-panel").fadeIn(200);
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
        // P is for PARTY
        case 80:
            $("html, body, div, header").css({
                'background-color': 'rgb(234, 255, 0)',
                'color': 'hotpink',
                'font-weight': 'bold',
                'text-transform': 'uppercase',
                'font-family': "'Comic Sans MS', 'Comic Sans', cursive",
                //'font-size': '50px',
                //'border': '30px solid #8cff00',
                //'border-radius': '140px',
            });
        };
      });

    
    // On "Run Simulation" button click
    $('#button-run').click(function() {
        $("#loading-overlay").fadeIn(100);
    })

    // On "Generate Scenario" button click
    $(".button-populate").click(function () {
        const csrftoken = getCookie('csrftoken');
        var message = {};
        const loading = !this.dataset.file;
        // Load csv file
        if (!loading) {
            message["command"] = "load"
            message["address"] = this.dataset.file;
        } 
        // Create random
        else {
            message["command"] = "random"
            // post 6 data fields
            message["fields"] = {
                "num" : parseInt(document.getElementsByName("random_num")[0].value),
                "min_x" : parseInt(document.getElementsByName("random_min-x")[0].value),
                "max_x" : parseInt(document.getElementsByName("random_max-x")[0].value),
                "min_y" : parseInt(document.getElementsByName("random_min-y")[0].value),
                "max_y" : parseInt(document.getElementsByName("random_max-y")[0].value),
                "min_radius" : parseInt(document.getElementsByName("random_min-radius")[0].value),
                "max_radius" : parseInt(document.getElementsByName("random_max-radius")[0].value)
            }
        }
        message = JSON.stringify(message);
        
        fetch("post_create", {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: message
        })
        .then(response => {
            openSimulate();
            (response.text().then(text => {
                const patch_source = JSON.parse(text).patch_source;
                const parameters = JSON.parse(text).parameters;
                var ds = Bokeh.documents[0].get_model_by_name('patch_data_source');
                ds.data = patch_source;
                ds.change.emit();

                document.getElementsByName("dispersal-kernel")[0].value = parameters["dispersal_kernel"];
                document.getElementsByName("colonization-probability")[0].value = parameters["colonization_probability"];
                document.getElementsByName("patch-extinction-probability-u")[0].value = parameters["patch_extinction_probability_u"];
                document.getElementsByName("patch-extinction-probability-a")[0].value = parameters["patch_extinction_probability_x"];
                document.getElementsByName("connectivity")[0].value = parameters["connectivity"];
                document.getElementsByName("rescue-effect")[0].value = parameters["rescue_effect"];
                document.getElementsByName("stochasticity")[0].value = parameters["stochasticity"];
            }));
        })
    })

});
