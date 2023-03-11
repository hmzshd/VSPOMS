$(document).ready(function () {

    $("#button-run").click(function(){
        const csrftoken = getCookie('csrftoken');
        var ds = Bokeh.documents[0].get_model_by_name('patch_data_source');
        var dispersal_kernel= document.getElementsByName("dispersal-kernel")[0].value;
        var colonization_probability = document.getElementsByName("colonization-probability")[0].value;
        var patch_extinction_probability_u = document.getElementsByName("patch-extinction-probability-u")[0].value;
        var patch_extinction_probability_x = document.getElementsByName("patch-extinction-probability-a")[0].value;
        var connectivity = document.getElementsByName("connectivity")[0].value;
        var rescue_effect = document.getElementsByName("rescue-effect")[0].value;
        var stochasticity = document.getElementsByName("stochasticity")[0].value;
        fetch("post_patches",{
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({"bokeh":ds.data,"dispersal_kernel":dispersal_kernel,
                "colonization_probability":colonization_probability,
                "patch_extinction_probability_u":patch_extinction_probability_u,
                "patch_extinction_probability_x":patch_extinction_probability_x,
                "connectivity":connectivity,
                "rescue_effect":rescue_effect,
                "stochasticity":stochasticity
            })
        })
        .then(response => {
            (response.text().then(async text => {
                const graphData = JSON.parse(text).message.data;
                const graphLayout = JSON.parse(text).message.layout;
                const graphFrames = JSON.parse(text).message.frames;
                const x = JSON.parse(text).turnovers.statuses;
                const y = JSON.parse(text).turnovers.x_coords;
                const status = JSON.parse(text).turnovers.y_coords;
                const replicates = JSON.parse(text).replicates;
                const dataTable = Bokeh.documents[0].get_model_by_name("vspoms").data_source;
                console.log(status.length / replicates);
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
                    dataTable.change.emit();
                    await sleep(200);
                }
                alert("The animating has been animated on the map")
                Plotly.newPlot('graph1', graphData, graphLayout).then(function () {
                    Plotly.animate('graph1', graphFrames)
                })
            }));
            // Front-end transition
            $("#loading-overlay").fadeOut(200);
            return null
        })
    });
})

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

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
