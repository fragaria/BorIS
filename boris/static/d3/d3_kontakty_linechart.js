(function() {
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line = d3.svg.line()
        .x(function(d) { return x(d.month); })
        .y(function(d) { return y(d.enc); });

    var svg = d3.select("#linechart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var encounters = IMPACT.encounters;
    var months = IMPACT.months;
    var encounters = encounters.map(item => {return Number(item);});

    get_data = (function() {
        var data = [];
        var len = months.length;
        for (var i = 0; i<len; i++) {
            data.push({
                month: months[i],
                enc: encounters[i]
              });
        }        
        return data;
    })();

    var data = get_data; 

    x.domain(data.map(function(d) { return d.month; }));
    y.domain([0, d3.max(data, function(d) { return d.enc; })]);

    // for x-axis format
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // for y-axis format
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Počet kontaktů");

    // determines properties of the line
    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .style("stroke-width", 2)
        .style("stroke", "steelblue")
        .style("fill", "none")
        .attr("d", line);
   })