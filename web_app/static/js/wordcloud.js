function fatCloud(){
    let url = '/api/ads';
    d3.json(url).then(function(response) {

        // use top words to generate wordcloud
        let dictionary = response["TopWords"];
        let adGroups = Object.keys(dictionary);

        //loop through each ad group
        adGroups.forEach(group => {

            // set an object to hold dictionary
            let groupDict = dictionary[`${group}`];

            // lists to hold words and values
            let words = Object.keys(groupDict),
                values = Object.values(groupDict);

            let wordCloudData = []; //list for reformated json data

            //for loop through each word to append to data
            for (i = 0; i < 40; i++) {
                wordCloudData.push({
                    "tag": words[i],
                    "weight": values[i]
                });
            }

            // set animations
            am4core.useTheme(am4themes_animated);
            //create chart object
            let chart = am4core.create(`${group}`, am4plugins_wordCloud.WordCloud);

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
            series.maxFontSize = 200; //minimum word size

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
    })
}

fatCloud();