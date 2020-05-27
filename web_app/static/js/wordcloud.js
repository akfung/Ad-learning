//array for holding keys for top word objects in api response
let adGroupArray = ['generalTopWords', 'insultTopWords', 'positivityTopWords', 'toxicityTopWords'];

//function to draw wordcloud
function fatCloud(adGroup){
    // create title
    switch (adGroup) {
        case 'generalTopWords':
            title = 'Most Common Among All Ads';
            break;
        
        case 'insultTopWords':
            title = 'Most Common Among Ads Labeled as Insulting';
            break;

        case 'positivityTopWords':
            title = 'Most Common Among Ads Labeled as Positive';
            break;

        case 'toxicityTopWords':
            title = 'Most Common Among Ads Labeled as Toxic';
            break;
    }

    d3.select("#word-cloud-title").text(title);

    let url = '/api/ads';
    d3.json(url).then(function(response) { //call api

        // use top words to generate wordcloud
        let groupDict = response["TopWords"][`${adGroup}`];

        // lists to hold words and values
        let words = Object.keys(groupDict),
            values = Object.values(groupDict);

        let wordCloudData = []; //array for reformated data

        //for loop through each word to append to data array
        for (i = 0; i < 40; i++) {
            wordCloudData.push({
                "tag": words[i],
                "weight": values[i]
            });
        }

        // set animations
        am4core.useTheme(am4themes_animated);
        //create chart object
        chart = am4core.create('wordCloudOutput', am4plugins_wordCloud.WordCloud);

        // read data from a series
        let series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());
        series.data = wordCloudData;

        // set words and values
        series.dataFields.word = "tag";
        series.dataFields.value = "weight"; 

        // set random colors
        series.colors = new am4core.ColorSet();
        series.colors.passOptions = {};

        series.randomness = 0; //make words as compact as possible
        series.minFontSize = 30; //maximum word size
        series.maxFontSize = 300; //minimum word size

        // progress indicator animations
        series.events.on("arrangestarted", function(ev) {
            ev.target.baseSprite.preloader.show(0);
        });
            
        series.events.on("arrangeprogress", function(ev) {
            ev.target.baseSprite.preloader.progress = ev.progress;
        });

        // add mouse hover tooltips
        series.labels.template.tooltipText = "{word}:\n[bold]{value}[/]";
    })
}

fatCloud('generalTopWords');


// listener for button clicks
function answer_click(elem){
    chart.dispose();
    console.log(elem.value);
    fatCloud(elem.value);
}

// updater function
// function updateCloud(){
//     fatCloud(answer_click);
// }

// //listener for buttons
// d3.selectAll(".word-cloud-button").on("click", updateCloud);



