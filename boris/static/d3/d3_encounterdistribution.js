  nv.addGraph(function() {

    var bounds = IMPACT.encounter_distribution.bounds;
    var counts = IMPACT.encounter_distribution.counts;
    var labels = IMPACT.encounter_distribution.labels;
    var anonymous = IMPACT.encounter_distribution.anonymous;

    bounds = bounds.map(item => {return Number(item);});
    counts = counts.map(item => {return Number(item);});

    get_data = (function() {
        var data_dummy = [];
        var len = bounds.length;
        for (var i = 0; i<len; i++) {
          data_dummy.push({
              label: labels[i],
              count: counts[i],
            });
          }        
        return data_dummy;
    })();
    var data_dist = get_data; 

    // originally used for multiBarChart
    // get_anonymous_bar = (function() {
    //     var data_dummy = [];
    //     var len = bounds.length;
    //     data_dummy = [{ label : ['anonym.'], count: [anonymous]},]
    //     for (var i = 0; i<len; i++) {
    //       data_dummy.push({
    //           label: labels[i],
    //           count: 0,
    //         });
    //       }        
    //     return data_dummy;
    // })();
    // var data_ano = get_anonymous_bar;



    dataAnnotated = [

      {
        key: "Klienti",
        // values: [{ label : ['anonym.'], count: [anonymous]},].push(data_dist),
        values: data_dist,
        // color: "#000000"
      },
    ];

    // var chart = nv.models.multiBarChart()
    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.label })    //Specify the data accessors.
        .y(function(d) { return d.count })
        .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
        //.tooltips(false)        //Don't show tooltips
        //.showValues(true)       //...instead, show the bar value right on top of each bar.
        //.transitionDuration(350)
       // .forceY([0,maxY])
        
    // chart.xAxis.rotateLabels(-90);
    chart.xAxis.axisLabel("Kontakty");
    chart.yAxis.axisLabel("Klienti");
    chart.yAxis.tickFormat(d3.format(',.0d'));
    chart.valueFormat(d3.format(',.0d'));
    chart.margin({ "top": 15, "right": 10, "bottom": 70, "left": 60 })

    d3.select('#encounter_distribution svg')
        .datum(dataAnnotated)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
  });

