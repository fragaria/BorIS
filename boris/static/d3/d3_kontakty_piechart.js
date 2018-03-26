nv.addGraph(function() {

  var drug_series = IMPACT.drug_type_occurrence.series;
  var drug_labels = IMPACT.drug_type_occurrence.labels;

  drug_series = drug_series.map(item => {return Number(item);});
 
  get_data = (function() {
      var data = [];
      var len = drug_labels.length;
      for (var i = 0; i<len; i++) {
        data.push({
            label: drug_labels[i],
            value: drug_series[i]
          });
        }        
      return data;
  })();
  var data_drugs = get_data; 

  dataAnnotated = [
    {
      key: "Drug occurrence",
      values: data_drugs,
      color: "#0000ff"
    }
  ];

  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)          //Turn on Donut mode. Makes pie chart look tasty!
      .donutRatio(0.35)     //Configure how big you want the donut hole size to be.
      .height(600)
      ;

  d3.select("#my_piechart svg")
      .datum(data_drugs)
      .call(chart);
  
  nv.utils.windowResize(chart.update);

  return chart;
});


