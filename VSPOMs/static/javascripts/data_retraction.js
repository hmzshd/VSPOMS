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
                const xs = [];
                const ys = [];
                const data = [];
                for(let i=0; i < JSON.parse(text).message.frames.length; i++){
                    xs.push(JSON.parse(text).message.frames[i].data[0].x[i])
                    ys.push(JSON.parse(text).message.frames[i].data[0].y[i])
                    data.push(JSON.parse(text).message.frames[i].data[0])
                }
                var frame = [{data: {y: ys}}]
                const graphLayout = JSON.parse(text).message.layout
                const graphFrames = JSON.parse(text).message.frames
                console.log(data)
                console.log(graphFrames)
                Plotly.newPlot('graph2', data, graphLayout)
            }));
            alert("Simulation Complete")
            return null
        })
    });
})

