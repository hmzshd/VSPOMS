// VSPOMs Backend/AJAX Scripts, JH04 2023

$(document).ready(function() {

    // On "Run Simulation" click
    $("#button-run").click(function() {
        $(this).attr("disabled", true);
        $(this).children('p').text("Loading...");
        // Start loading overlay
        pickFrog();
        $("#loading-overlay").fadeIn(100);
        const csrftoken = getCookie('csrftoken');
        // Get variables from input fields
        var ds = Bokeh.documents[0].get_model_by_name('patch_data_source');
        var species_specific_dispersal_constant= document.getElementsByName("dispersal-kernel")[0].value;
        var species_specific_constant_colonisation_y = document.getElementsByName("colonization-probability")[0].value;
        var species_specific_extinction_constant_u = document.getElementsByName("patch-extinction-probability-u")[0].value;
        var patch_area_effect_extinction_x = document.getElementsByName("patch-extinction-probability-a")[0].value;
        var area_exponent_connectivity_b = document.getElementsByName("connectivity")[0].value;
        var rescue_effect = document.getElementsByName("rescue-effect")[0].value;
        var stochasticity = document.getElementsByName("stochasticity")[0].value;
        var steps = document.getElementsByName("sim_steps")[0].value;
        var replicates = document.getElementsByName("sim_replicates")[0].value;

        // Post to post_patches
        fetch("post_patches", {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            // Set and send dictionary
            body: JSON.stringify({
                "bokeh":ds.data,"species_specific_dispersal_constant":species_specific_dispersal_constant,
                "area_exponent_connectivity_b":area_exponent_connectivity_b,
                "species_specific_extinction_constant_u":species_specific_extinction_constant_u,
                "patch_area_effect_extinction_x":patch_area_effect_extinction_x,
                "species_specific_constant_colonisation_y":species_specific_constant_colonisation_y,
                "rescue_effect":rescue_effect,
                "stochasticity":stochasticity,
                "steps" : steps,
                "replicates" : replicates
            })
        })
        .then(response => {
            (response.text().then(async text => {
                // Parse returned JSON message
                const graph1Data = JSON.parse(text).graph1.data;
                const graph1Layout = JSON.parse(text).graph1.layout;
                const graph2Data = JSON.parse(text).graph2.data;
                const graph2Layout = JSON.parse(text).graph2.layout;
                const graph3Data = JSON.parse(text).graph3.data;
                const graph3Layout = JSON.parse(text).graph3.layout;
                const graph4Data = JSON.parse(text).graph4.data;
                const graph4Layout = JSON.parse(text).graph4.layout;
                const x = JSON.parse(text).turnovers.statuses;
                const y = JSON.parse(text).turnovers.x_coords;
                const status = JSON.parse(text).turnovers.y_coords;
                const steps = JSON.parse(text).steps;
                const replicates = JSON.parse(text).replicates;
                const dataTable = Bokeh.documents[0].get_model_by_name("vspoms").data_source;
                // Animate patch graph
                Plotly.newPlot('graph1', graph1Data, graph1Layout)
                Plotly.newPlot('graph2', graph2Data, graph2Layout)
                Plotly.newPlot('graph3', graph3Data, graph3Layout)
                Plotly.newPlot('graph4', graph4Data, graph4Layout)
                $("#progress-bar").css("display", "flex");
                for (let i = 0; i < status.length  / replicates; i++) {
                    for (let j = 0; j < (dataTable.data["color"].length); j++) {
                        let mapx = dataTable.data["x"][j];
                        let mapy = dataTable.data["y"][j];
                        if (mapx == x[i] && mapy == y[i]) {
                            if (status[i] != true) {
                                dataTable.data["color"][j] = "green";
                            } else {
                                dataTable.data["color"][j] = "red";
                            }
                        }
                    }
                    // Set animation speed
                    let simulation_speed = parseInt(document.getElementsByName("sim_speed")[0].value);
                    await sleep(simulation_speed);
                    dataTable.change.emit();  
                    let percent_done = Math.round(i / (status.length / replicates) * 100) + "%";
                    $("#progress-bar").css("width", percent_done);
                    $(this).children('p').text(percent_done);
                }
                // When sim animation has finished
                $(this).children('p').text("100%");
                $(this).attr("disabled", false);
                await sleep(200);
                $("#progress-bar").css("width", "0%").hide();
                $(this).children('p').text("Re-Run Simulation");
            }));
            // Hide loading overlay
            $("#loading-overlay").fadeOut(200);
            return null;
        })
    });


    // On "Load" or "Generate Scenario" click
    $(".button-populate").click(function() {
        pickFrog();
        $("#loading-overlay").fadeIn(100);
        const csrftoken = getCookie('csrftoken');
        var message = {};
        const loading = !this.dataset.file;
        // Load scenario if specified
        if (!loading) {
            message["command"] = "load"
            message["address"] = this.dataset.file;
        }
        // Otherwise create random scenario
        else {
            message["command"] = "random"
            // Get random scenario fields from input boxes
            message["fields"] = {
                "num" : parseInt(document.getElementsByName("random_num")[0].value),
                "min_x" : parseInt(document.getElementsByName("random_min-x")[0].value),
                "max_x" : parseInt(document.getElementsByName("random_max-x")[0].value),
                "min_y" : parseInt(document.getElementsByName("random_min-y")[0].value),
                "max_y" : parseInt(document.getElementsByName("random_max-y")[0].value),
                "min_area" : parseInt(document.getElementsByName("random_min-area")[0].value),
                "max_area" : parseInt(document.getElementsByName("random_max-area")[0].value)
            }
        }
        message = JSON.stringify(message);

        // Post message to post_create view
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
        // Check if response throws error
        .then(response => {
            // Hide loading and navigate to simulate page
            $("#loading-overlay").fadeOut(200);
            (response.text().then(text => {
                if (!response.ok) {
                    throw new Error(JSON.parse(text).error);
                }
                openSimulate();
                // Set patch graph
                const patch_source = JSON.parse(text).patch_source;
                const parameters = JSON.parse(text).parameters;
                var ds = Bokeh.documents[0].get_model_by_name('patch_data_source');
                ds.data = patch_source;
                ds.change.emit();
                // Set parameters
                document.getElementsByName("dispersal-kernel")[0].value = parameters["species_specific_dispersal_constant"];
                document.getElementsByName("colonization-probability")[0].value = parameters["species_specific_constant_colonisation_y"];
                document.getElementsByName("patch-extinction-probability-u")[0].value = parameters["species_specific_extinction_constant_u"];
                document.getElementsByName("patch-extinction-probability-a")[0].value = parameters["patch_area_effect_extinction_x"];
                document.getElementsByName("connectivity")[0].value = parameters["area_exponent_connectivity_b"];
                document.getElementsByName("rescue-effect")[0].value = parameters["rescue_effect"];
                document.getElementsByName("stochasticity")[0].value = parameters["stochasticity"];
            }))
            // Catch if error is thrown - show popup
            .catch(function(error) {
                $("#loading-overlay").fadeOut(200);
                $("#popup_load-error").fadeIn(200).children("p").text(error);
            });
        })
    });


});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to sleep before next animation frame
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}