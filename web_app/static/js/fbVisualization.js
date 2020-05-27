
// lists of categories and features to refer back to
let categories = ['Impressions', 'spending', 'TopWords'];        
let features = ['general', 'insult', 'positivity', 'toxicity'];



// querry database via api call to appropriate flask route and generate plotly visualization

function generalAdData(){
    let url = '/api/ads';
    d3.json(url).then(function(response) {

        console.log(response);
        
        let feature = features[0];
        d3.select('#dropdownMenuButton').text(feature);
        // loop through each category
        categories.forEach(category => {
            let dictionary = response[category];

            ad_metrics = dictionary[feature + category];

            // conditional formatting based on category
            if (category === 'Impressions') {
                yaxisScale = 'log';
                yaxisTitle = 'Percentage of Ads';
                xaxisScale = 'category';
                xaxisTitle = 'Number of Impressions'
            }
            
            else if(category === 'spending'){
                yaxisScale = 'log';
                yaxisTitle = 'Percentage of Ads';
                xaxisScale = 'category';
                xaxisTitle = 'USD Spent';
                graphTitle = `Ad Frequency Per Ad Spending`;
            }

            else if(category === 'TopWords'){
                yaxisScale = 'linear';
                yaxisTitle = 'Number of Occurances';
                xaxisScale = 'category';
                xaxisTitle = 'Word';
                graphTitle = `Top 10 Most Frequent Words in Political Ads`;
            }

            // generate traces
            let traceGeneral = { 
                x: Object.keys(dictionary[`general${category}`]),
                y: Object.values(dictionary[`general${category}`]),
                type: 'bar',
                name: "Full Dataset"
            };

            let traceInsult = { 
                x: Object.keys(dictionary[`insult${category}`]),
                y: Object.values(dictionary[`insult${category}`]),
                type: 'bar',
                name: "Insulting Ads"
            };

            let tracePositivity = { 
                x: Object.keys(dictionary[`positivity${category}`]),
                y: Object.values(dictionary[`positivity${category}`]),
                type: 'bar',
                name: "Positive Ads"
            };

            let traceToxicity = { 
                x: Object.keys(dictionary[`toxicity${category}`]),
                y: Object.values(dictionary[`toxicity${category}`]),
                type: 'bar',
                name: "Toxic Ads"
            };

            //set graph layouts
            let barLayout = {
                title: {
                    font: {size: 24}
                },
                height: 600,
                width: 1200,
                yaxis:{
                    title: {
                        text: yaxisTitle,
                        standoff: 20,
                        font: {size: 20}
                    },
                    type: yaxisScale,
                    autorange: true,
                    tickfont: {size: 16}
                },
                xaxis:{
                    type: xaxisScale,
                    title: {
                        text: xaxisTitle,
                        standoff: 800,
                        font: {size: 20}
                    },
                    autorange: true,
                    tickfont: {size: 16}
                },
                legend:{
                    font: {size: 20}
                },
                barmode: 'group'
            }

            //actually plot
            Plotly.newPlot(category, [traceGeneral, traceInsult, tracePositivity, traceToxicity], barLayout);
            

        });     

    })

};

 generalAdData(); //run the function for initial graphs upon page loading

 

