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
        alert("Simulation Begin");
        fetch("post_patches",{
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(ds.data)
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

