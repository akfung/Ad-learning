// querry database via api call to appropriate flask route and generate plotly visualization
function generalAdData(){
    let url = '/api/ads';
    d3.json(url).then(function(response) {
        console.log(response);

        // set plotly traces

    })

};
