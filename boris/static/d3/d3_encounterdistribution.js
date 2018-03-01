  nv.addGraph(function() {

    var bounds = IMPACT.encounter_distribution.bounds;
    var counts = IMPACT.encounter_distribution.counts;
    var labels = IMPACT.encounter_distribution.labels;

    console.log("labels", labels);

    bounds = bounds.map(item => {return Number(item);});
    counts = counts.map(item => {return Number(item);});

    get_data = (function() {
        var data_dummy = [];
        var len = bounds.length;
        for (var i = 0; i<len; i++) {
          data_dummy.push({
              // bound: bounds[i],
              label: labels[i],
              count: counts[i],
            });
          }        
        return data_dummy;
    })();
    var data_dist = get_data; 

    dataAnnotated = [
      {
        key: "Distribution of encounters",
        values: data_dist,
        color: "#000000"
      }
    ];

    console.log('dataAnnotated',dataAnnotated);

    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.label })    //Specify the data accessors.
        .y(function(d) { return d.count })
        .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
        //.tooltips(false)        //Don't show tooltips
        .showValues(true)       //...instead, show the bar value right on top of each bar.
        //.transitionDuration(350)
       // .forceY([0,maxY])
        ;

    chart.xAxis.axisLabel("Kontakty");
    chart.yAxis.axisLabel("Klienti");
    chart.margin({ "top": 15, "right": 10, "bottom": 70, "left": 60 })

    d3.select('#encounter_distribution svg')
        .datum(dataAnnotated)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
  });

