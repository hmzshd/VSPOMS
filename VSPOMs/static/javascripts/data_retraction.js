$(document).ready(function () {
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
        alert("Simulation Begins with \n"+
            "Disposal kernel = " + dispersal_kernel.toString()+"\n"+
            "Colonization probability = " + colonization_probability.toString()+"\n"+
            "Patch extinction u = " + patch_extinction_probability_u.toString()+"\n"+
            "Patch extinction x = " + patch_extinction_probability_x.toString()+"\n"+
            "Connectivity = " + connectivity.toString()+"\n"+
            "Rescue Effect = " + rescue_effect.toString()+"\n"+
            "Stochasticity = " + stochasticity.toString());
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
            (response.text().then(text => {
                const graphData = JSON.parse(text).message.data
                const graphLayout = JSON.parse(text).message.layout
                const graphFrames = JSON.parse(text).message.frames
                console.log(graphData)
                console.log(graphFrames)
                console.log(graphLayout)
                Plotly.newPlot('graph1', graphData, graphLayout).then(function () {
                    Plotly.animate('graph1',graphFrames)
                })
            }));
            alert("Simulation Complete")
            return null
        })
    });
})

