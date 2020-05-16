// querry database via api call to appropriate flask route and generate plotly visualization

function generalAdData(){
    let url = '/api/ads';
    d3.json(url).then(function(response) {

        console.log(response);
        let categories = Object.keys(response);        
        let features = ['general', 'insult', 'positivity', 'toxicity'];
        let feature = features[0];
        // loop through each category
        categories.forEach(category => {
            let dictionary = response[category]
            ad_metrics = dictionary[feature + category]

            // generate traces
            let tracePie = { //bar trace
                values: Object.keys(ad_metrics),
                labels: Object.values(ad_metrics),
                type: 'pie'
            };

            let pieLayout = {
                title: category,
                height: 600,
                width: 400
            }

            Plotly.newPlot(category, [tracePie], pieLayout);
            

        });

        

        

    })

};

 generalAdData();