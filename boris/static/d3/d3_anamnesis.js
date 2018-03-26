

  nv.addGraph(function() {
 
    var anamnesis = IMPACT.anamnesis;
    var anamnesis_object = IMPACT.anamnesis_object;

    console.log("anamnesis", anamnesis);
    console.log("IMPACT.anamnesis_object", IMPACT.anamnesis_object);

    var periodicity_dict = {
        'not found': -2,
        'unknown' : -1,
        'never' : 0,
        'once' : 1,
        'often' : 2
    }

    var manner_dict = {
        iv : 'Nitrožílní aplikace',
        ss : 'Sdílení jehel',
        ra : 'Riziková aplikace',
        us : 'Nechráněný sex',
        od : 'Předávkování',
    }

    var improvements = anamnesis_object.filter(a => {
        var include = false;
        for (manner in a.riskymanners) {
            var past = periodicity_dict[a.riskymanners[manner].past];
            var present = periodicity_dict[a.riskymanners[manner].present];
            //console.log('filter', past, present, a.riskymanners  );
            if(!include){
                include = (present > -1 && past > -1)
            }
        }
        return include;
    });
    console.log('improvements',improvements);


    get_improvements = (function() {
        var data_dummy = [];
        for (manner in manner_dict) {
            var label = '';
            var improvement = 0;
            for (a of anamnesis_object) {
                var past = periodicity_dict[a.riskymanners[manner].past];
                var present = periodicity_dict[a.riskymanners[manner].present];                
                if(present > -1 && past > -1){
                    if(past > present)
                        improvement += 1;
                    if(past < present)
                        improvement -= 1; 
                }
            }
            data_dummy.push({
                manner_label: manner_dict[manner],
                client_count: improvement,
            });
        }
        console.log('data_dummy',data_dummy);   
        return data_dummy;
    })();


    AnamnesisDataAnnotated = [
      {
        key: "Potlačení rizikového chování",
        values: get_improvements,
        color: "#000000"
      }
    ];


    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.manner_label })    //Specify the data accessors.
        .y(function(d) { return d.client_count })
        .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
        //.tooltips(false)        //Don't show tooltips
        .showValues(true)       //...instead, show the bar value right on top of each bar.
        //.transitionDuration(350)
       // .forceY([0,maxY])
        ;

    chart.xAxis.axisLabel("Rizikové chování");
    chart.yAxis.axisLabel("Počet zlepšení",);
    chart.yAxis.tickFormat(d3.format(',.0d'));
    chart.margin({ "top": 15, "right": 10, "bottom": 70, "left": 60 })
    chart.valueFormat(d3.format(',.0d'));
    d3.select('#riskymanners_improvement svg')
        .datum(AnamnesisDataAnnotated)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;

  });

