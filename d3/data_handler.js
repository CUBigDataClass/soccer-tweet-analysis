var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S.%L+0000");

//fetch data
d3.csv("daily_count.csv")
    //format data as it comes in
    .row(function(d){return {club: d.club, count:Number(d.count) , date: parseDate(d.date)}})
    .get(function(error, data){

        var height = 500;
        var width = 700;

        var max = d3.max(data, function(d){return d.count;});
        var minDate = d3.min(data, function(d){return d.date;});
        var maxDate = d3.max(data, function(d){return d.date;});

        var y = d3.scaleLinear()
                    .domain([0, max])
                    .range([height, 0]);

        var x = d3.scaleTime()
                    .domain([minDate, maxDate])
                    .range([0, width]);

        var yAxis = d3.axisLeft(y);
        var xAxis = d3.axisBottom(x);

        var svg = d3.select("body").append("svg").attr("height", "700").attr("width", "100%");

        var margin = {left:50, right:50, top:40, bottom:0};

        var chartGroup = svg.append("g")
                              .attr("transform", "translate("+margin.left+", "+margin.top+")");

        var line = d3.line()
                      .x(function(d){return x(d.date);})
                      .y(function(d){return y(d.count);});

        var sorted_data = data.sort(function(a, b) { return a.date - b.date;});

        //CROSSFILTER

        function print_filter(filter){
	var f=eval(filter);
	if (typeof(f.length) != "undefined") {}else{}
	if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
	if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
	console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
}

        var ndx = crossfilter(sorted_data);
        var clubDim = ndx.dimension(function(d) { return d.club; });
        var AS_Roma_filter = clubDim.filter('AS Roma');
        var AS_Roma_total = ndx.groupAll().reduceSum(function(d){return d.count;}).value()
        console.log("AS Roma " + AS_Roma_total);

        //print_filter("AS_Roma_filter");

        clubDim.filterAll();

        var Liverpool_filter = clubDim.filter('Liverpool');
        var Liverpool_total = ndx.groupAll().reduceSum(function(d){return d.count;}).value()
        console.log("Liverpool " + Liverpool_total);
        clubDim.filterAll();







      //  var all = cf_data.groupAll();


        chartGroup.append("path").attr("d", line(sorted_data));
        chartGroup.append("g").attr("class", "x axis").attr("transform", "translate(0, "+height+")").call(xAxis);
        chartGroup.append("g").attr("class", "y axis").call(yAxis);

        //SLIDER??
        /*
        var slider = svg.append("g")
                            .attr("class", "slider")
                            .attr("transform", "translate(" + margin.left + ", 600)");

        slider.append("line")
                .attr("class", "track")
                .attr("x1", x.range()[0]) //min
                .attr("x2", x.range()[1]) //max
                .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
                .attr("class", "track-inset")
                .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
                .attr("class", "track-overlay")
                .call(d3.drag()
                    .on("start.interrupt", function() { slider.interrupt(); })
                    .on("start drag", function() { hue(x.invert(d3.event.x)); }));

        var handle = slider.insert("circle", ".track-overlay")
                        .attr("class", "handle")
                        .attr("r", 9);

        slider.transition() // Gratuitous intro!
            //.duration(5)
            .tween("position", function() {
            var i = d3.interpolate(0, 70);

            //if statement to keep within the boundaries, probably through margins defined earlier i'd guess
            return handle.attr("cx", x(i));
            });

        function hue(h) {
                handle.attr("cx", x(h));
                //svg.style("background-color", d3.hsl(h, 0.8, 0.8));
                }
                */

    });
