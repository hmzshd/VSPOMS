// VSPOMs Backend/AJAX Scripts, JH04 2023

$(document).ready(function() {

    // On "Run Simulation" click
    $("#button-run").click(function() {
        // Start loading overlay
        $("#loading-overlay").fadeIn(100);
        const csrftoken = getCookie('csrftoken');
        // Get variables from input fields
        var ds = Bokeh.documents[0].get_model_by_name('patch_data_source');
        var dispersal_kernel= document.getElementsByName("dispersal-kernel")[0].value;
        var colonization_probability = document.getElementsByName("colonization-probability")[0].value;
        var patch_extinction_probability_u = document.getElementsByName("patch-extinction-probability-u")[0].value;
        var patch_extinction_probability_x = document.getElementsByName("patch-extinction-probability-a")[0].value;
        var connectivity = document.getElementsByName("connectivity")[0].value;
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
                "bokeh":ds.data,"dispersal_kernel":dispersal_kernel,
                "colonization_probability":colonization_probability,
                "patch_extinction_probability_u":patch_extinction_probability_u,
                "patch_extinction_probability_x":patch_extinction_probability_x,
                "connectivity":connectivity,
                "rescue_effect":rescue_effect,
                "stochasticity":stochasticity,
                "steps" : steps,
                "replicates" : replicates
            })
        })
        .then(response => {
            (response.text().then(async text => {
                // Parse returned JSON message
                const graphData = JSON.parse(text).message.data;
                const graphLayout = JSON.parse(text).message.layout;
                const graphFrames = JSON.parse(text).message.frames;
                const x = JSON.parse(text).turnovers.statuses;
                const y = JSON.parse(text).turnovers.x_coords;
                const status = JSON.parse(text).turnovers.y_coords;
                const steps = JSON.parse(text).steps;
                const replicates = JSON.parse(text).replicates;
                const dataTable = Bokeh.documents[0].get_model_by_name("vspoms").data_source;
                // Animate patch graph
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
                }
                // When animation has finished
                alert("The animating has been animated on the map");
                // Plot graphs
                Plotly.newPlot('graph1', graphData, graphLayout).then(function() {
                    Plotly.animate('graph1', graphFrames)
                })
            }));
            // Hide loading overlay
            $("#loading-overlay").fadeOut(200);
            return null
        })
    });


    // On "Generate Scenario" click
    $(".button-populate").click(function() {
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
        .then(response => {
            // Hide loading and navigate to simulate page
            $("#loading-overlay").fadeOut(200);
            openSimulate();
            (response.text().then(text => {
                // Set patch graph
                const patch_source = JSON.parse(text).patch_source;
                const parameters = JSON.parse(text).parameters;
                var ds = Bokeh.documents[0].get_model_by_name('patch_data_source');
                ds.data = patch_source;
                ds.change.emit();
                // Set parameters
                document.getElementsByName("dispersal-kernel")[0].value = parameters["dispersal_kernel"];
                document.getElementsByName("colonization-probability")[0].value = parameters["colonization_probability"];
                document.getElementsByName("patch-extinction-probability-u")[0].value = parameters["patch_extinction_probability_u"];
                document.getElementsByName("patch-extinction-probability-a")[0].value = parameters["patch_extinction_probability_x"];
                document.getElementsByName("connectivity")[0].value = parameters["connectivity"];
                document.getElementsByName("rescue-effect")[0].value = parameters["rescue_effect"];
                document.getElementsByName("stochasticity")[0].value = parameters["stochasticity"];
            }));
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
