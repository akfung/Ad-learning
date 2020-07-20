//array for holding keys for top word objects in api response
let adGroupArray = [
  "generalTopWords",
  "insultTopWords",
  "positivityTopWords",
  "toxicityTopWords",
];

//create bar chart under wordcloud

let url = "/api/ads";
d3.json(url).then(function (response) {
  let dictionary = response["TopWords"];

  // formatting options
  yaxisScale = "linear";
  yaxisTitle = "Number of Occurances";
  xaxisScale = "category";
  xaxisTitle = "Word";

  // generate traces
  let traceGeneral = {
    x: Object.keys(dictionary[`generalTopWords`]),
    y: Object.values(dictionary[`generalTopWords`]),
    type: "bar",
    name: "Full Dataset",
  };

  let traceInsult = {
    x: Object.keys(dictionary[`insultTopWords`]),
    y: Object.values(dictionary[`insultTopWords`]),
    type: "bar",
    name: "Insulting Ads",
  };

  let tracePositivity = {
    x: Object.keys(dictionary[`positivityTopWords`]),
    y: Object.values(dictionary[`positivityTopWords`]),
    type: "bar",
    name: "Positive Ads",
  };

  let traceToxicity = {
    x: Object.keys(dictionary[`toxicityTopWords`]),
    y: Object.values(dictionary[`toxicityTopWords`]),
    type: "bar",
    name: "Toxic Ads",
  };

  //set graph layout
  let barLayout = {
    height: 600,
    width: 1200,
    yaxis: {
      title: {
        text: yaxisTitle,
        standoff: 20,
        font: { size: 20 },
      },
      type: yaxisScale,
      autorange: true,
      tickfont: { size: 16 },
    },
    xaxis: {
      type: xaxisScale,
      title: {
        text: xaxisTitle,
        standoff: 800,
        font: { size: 20 },
      },
      autorange: true,
      tickfont: { size: 16 },
    },
    legend: {
      font: { size: 20 },
    },
    barmode: "group",
  };

  //actually plot
  Plotly.newPlot(
    "TopWordsGraph",
    [traceGeneral, traceInsult, tracePositivity, traceToxicity],
    barLayout
  );
});

//function to draw wordcloud
function fatCloud(adGroup) {
  // create title
  switch (adGroup) {
    case "generalTopWords":
      title = "Top Words Among All Ads";
      break;

    case "insultTopWords":
      title = "Top Words Among Ads Labeled as Insulting";
      break;

    case "positivityTopWords":
      title = "Top Words Among Ads Labeled as Positive";
      break;

    case "toxicityTopWords":
      title = "Top Words Among Ads Labeled as Toxic";
      break;
  }

  d3.select("#word-cloud-title").text(title); //set title depending on adGroup

  let url = "/api/ads";
  d3.json(url).then(function (response) {
    //call api

    // use top words to generate wordcloud
    let groupDict = response["TopWords"][`${adGroup}`];

    // lists to hold words and values
    let words = Object.keys(groupDict),
      values = Object.values(groupDict);

    let wordCloudData = []; //array for reformated data

    //for loop through each word to append to data array
    for (i = 0; i < 40; i++) {
      wordCloudData.push({
        tag: words[i],
        weight: values[i],
      });
    }

    // set animations
    am4core.useTheme(am4themes_animated);
    //create chart object
    chart = am4core.create("wordCloudOutput", am4plugins_wordCloud.WordCloud);

    // read data from a series
    let series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());
    series.data = wordCloudData;

    // set words and values
    series.dataFields.word = "tag";
    series.dataFields.value = "weight";

    // set random colors
    series.colors = new am4core.ColorSet();
    series.colors.passOptions = {};

    series.randomness = 0.2; //set word compactness as
    series.minFontSize = 30; //maximum word size
    series.maxFontSize = 300; //minimum word size

    // progress indicator animations
    series.events.on("arrangestarted", function (ev) {
      ev.target.baseSprite.preloader.show(0);
    });

    series.events.on("arrangeprogress", function (ev) {
      ev.target.baseSprite.preloader.progress = ev.progress;
    });

    // add mouse hover tooltips
    series.labels.template.tooltipText = "{word}\n[bold]{value}[/]";
  });
}

//on page load render general top words
fatCloud("generalTopWords");

// listener for button clicks
function answer_click(elem) {
  chart.dispose();
  fatCloud(elem.value);
}
