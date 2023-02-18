$(document).ready(function () {
    $("#button-run").click(function(){
        var ds = Bokeh.documents[0].get_model_by_name('patch_data_source');
        $.ajax({
            type: "POST",
            url: "vspoms/patches",
            data: ds,
            success: function (response){
                $("#button-run").hide()
                console.log(response["message"])
            },
            error: function(response) {
                alert(response["error"])
            }
        });
    });
})