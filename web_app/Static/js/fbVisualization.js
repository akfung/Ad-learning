// querry database via api call to appropriate flask route and generate plotly visualization
function generalAdData(){
    let url = '/api/ads';
    d3.json(url).then(function(response) {
        console.log(response);

        // generate traces
        let traceBar = { //bar trace
            y: findBarData(0).IDs,
            x: findBarData(0).values,
            type: 'bar'
        };

        Plotly.newPlot('bar', [traceBar], barLayout);

    })

};

 