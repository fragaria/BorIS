  nv.addGraph(function() {

    var bounds = IMPACT.encounter_distribution.bounds;
    var counts = IMPACT.encounter_distribution.counts;
    var labels = IMPACT.encounter_distribution.labels;
    var anamnesis = IMPACT.anamnesis;
    var anamnesis_object = IMPACT.anamnesis_object;

    console.log("anamnesis", anamnesis);
    console.log("IMPACT.anamnesis_object", IMPACT.anamnesis_object);

    var periodicity_dict = {
        'unknown' : -1,
        'never' : 0,
        'once' : 1,
        'often' : 2
    }


    var iv_improvement = anamnesis_object.filter(a => {
        var past = periodicity_dict(a.iv_past);
        var present = periodicity_dict(a.iv_present);
        return (past> 0 && present > 0 && past > present)
    }).length;
    console.log('iv_improvement',iv_improvement);

    
                // iv_past : "{{ a2.iv_past }}", 
                // iv_present : "{{ a2.iv_present }}", 
                // ss_past : "{{ a2.ss_past }}", 
                // ss_present : "{{ a2.ss_present }}", 
                // us_past : "{{ a2.us_past }}", 
                // us_present : "{{ a2.us_present }}", 
                // ra_past : "{{ a2.ra_past }}", 
                // ra_present : "{{ a2.ra_present }}", 
                // od_past : "{{ a2.od_past }}", 
                // od_present : "{{ a2.od_present }}", 

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



  });

