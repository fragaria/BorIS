  nv.addGraph(function() {

    var encounters = IMPACT.encounters;
    var months = IMPACT.months;

    encounters = encounters.map(item => {return Number(item);});

    get_data = (function() {
        var data_dummy = [];
        var len = months.length;
        for (var i = 0; i<len; i++) {
          data_dummy.push({
              month: months[i],
              enc: encounters[i]
            });
          }        
        return data_dummy;
    })();
    var data_enc = get_data; 

    dataAnnotated = [
      {
        key: "Cumulative Return",
        values: data_enc,
        color: "#0000ff"
      }
    ];

    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.month })    //Specify the data accessors.
        .y(function(d) { return d.enc })
        .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
        .showValues(true)       //...instead, show the bar value right on top of each bar.
        ;

    chart.yAxis.tickFormat(d3.format(',.0d'));
    chart.valueFormat(d3.format(',.0d'));

    d3.select('#my_chart svg')
        .datum(dataAnnotated)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
  });

