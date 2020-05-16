
// lists of categories and features to refer back to
let categories = ['Impressions', 'spending', 'TopWords'];        
let features = ['general', 'insult', 'positivity', 'toxicity'];

// generate dropdown for changing dataset
features.forEach(feature => {
    d3.select('#selDataset').append('option')
        .attr("value", feature)
        .attr('id', feature)
        .text(feature)
});



// querry database via api call to appropriate flask route and generate plotly visualization

function generalAdData(){
    let url = '/api/ads';
    d3.json(url).then(function(response) {

        console.log(response);
        
        let feature = features[0];
        d3.select('#dropdownMenuButton').text(feature);
        // loop through each category
        categories.forEach(category => {
            let dictionary = response[category],
                uniqueDictionary = response[category + 'Unique']

            ad_metrics = dictionary[feature + category]
            ad_metrics_unique = uniqueDictionary[feature + category + 'Unique'] 

            // conditional formatting based on category
            if (category === 'Impressions') {
                yaxisScale = 'log';
                yaxisTitle = 'Number of Ads';
                xaxisScale = 'log';
                xaxisTitle = 'Number of Impressions';
                graphTitle = `Ad Frequency Per Impression Group`;
            }
            
            else if(category === 'spending'){
                yaxisScale = 'log';
                yaxisTitle = 'Number of Ads';
                xaxisScale = 'log';
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
            let traceBar = { 
                x: Object.keys(ad_metrics),
                y: Object.values(ad_metrics),
                type: 'bar',
                name: category
            };

            let traceUniqueBar = {
                x: Object.keys(ad_metrics_unique),
                y: Object.values(ad_metrics_unique),
                type: 'bar',
                name: category + ' Unique'
            }

            let barLayout = {
                title: {
                    text: graphTitle,
                    font: {size: 24}
                },
                height: 600,
                width: 1200,
                yaxis:{
                    title: {
                        text: yaxisTitle,
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

            Plotly.newPlot(category, [traceBar, traceUniqueBar], barLayout);
            

        });

        d3.selectAll("#selDataset").on("change", updateBar); //listener for dropdown selections

        // function to update bar graphs on selection change
        function updateBar(){
        
            let feature = d3.select("#selDataset").property("value"); // save the selected value in variable
            // restyle the bar plot

            categories.forEach(category => {
                dictionary = response[category];
                uniqueDictionary = response[category + 'Unique'];
    
                ad_metrics = dictionary[feature + category];
                ad_metrics_unique = uniqueDictionary[feature + category + 'Unique'];

                Plotly.restyle(category, "x", [Object.keys(ad_metrics), Object.keys(ad_metrics_unique)]);
                Plotly.restyle(category, "y", [Object.values(ad_metrics), Object.values(ad_metrics_unique)]);
            })    
        };    

        

    })

};

 generalAdData(); //run the function for initial graphs upon page loading

 

 // optionChanged function for updating value of dropdown
function optionChanged() {
    let selection = document.getElementById("selDataset");
    selection.text = selection.value
}

