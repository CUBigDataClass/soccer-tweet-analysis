var GLOBAL_J = 0
var GAME_DATES=[]
var TEAM="Roma"

function print_filter(filter){
var f = eval(filter);
if (typeof(f.length) != "undefined") {}else{}
if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
}

//fetch data

d3.queue()
	.defer(d3.json, "as_roma.json")
	.defer(d3.json, "roma_games.json")
	.await(function(error, countsData, gamesData){
		if (error) throw error;

		//time formats
		var countsDateFormat = d3.time.format("%Y-%m-%d %H:%M:%S.%L+0000");
		var gameDateFormat = d3.time.format("%m/%d/%Y");

		//create date dimensions and groups
		//count data
		var ndxc = crossfilter(countsData)
		var dateDim = ndxc.dimension(function(d) {
				 d.date = countsDateFormat.parse(d.date);
				return d.date;
			});
		var countsGroup = dateDim.group().reduceSum(dc.pluck('count'));

		//games data
		var ndxGames = crossfilter(gamesData)
 	    var gameDateDim = ndxGames.dimension(function(d){d.date = gameDateFormat.parse(d.date); d.count = 0; return d.date;})

		//sorted lists for connecting games with counts
		var countsArrayByDate = dateDim.bottom(Infinity)
		var gamesArrayByDate = gameDateDim.bottom(Infinity)

		//logic for connecting games with counts (unfortunate use of globals)
		function connectGames(date, count){
			if ( GLOBAL_J < gamesArrayByDate.length){
				searchDate = gamesArrayByDate[GLOBAL_J].date
				if ( date < searchDate){
					return
				}
				if (+date == +searchDate){
					GAME_DATES[GLOBAL_J] = {}
					GAME_DATES[GLOBAL_J].date = date
					GAME_DATES[GLOBAL_J].count = count
					GAME_DATES[GLOBAL_J].club1 = gamesArrayByDate[GLOBAL_J].club1
					GAME_DATES[GLOBAL_J].club2 = gamesArrayByDate[GLOBAL_J].club2
					GAME_DATES[GLOBAL_J].club1score = gamesArrayByDate[GLOBAL_J].club1score
					GAME_DATES[GLOBAL_J].club2score = gamesArrayByDate[GLOBAL_J].club2score
					return
				}
				else{
					if( date > searchDate){
						GLOBAL_J++
						connectGames(date, count)
					}
				}
			}
			else {
				GLOBAL_J++
				return
			}
		}


		//call logic to connect
	   	countsArrayByDate.forEach(function(d, i) {
		connectGames(d.date, d.count)
		});

		//compose counts group for games to link up
		var ndxg= crossfilter(GAME_DATES)
		var gameDateDim = ndxg.dimension(function(d){ return [d.date, +d.count, d.club1, d.club2, d.club1score, d.club2score]})
		var filteredCounts = gameDateDim.filterFunction(function(d){console.log(d); return d != undefined})
		var gameCountGroup = filteredCounts.group().reduceSum(function(d){ if (d != undefined) {return d.count} else return 0}); //something fucked happening

		//begin setting up charts
		var minDate = dateDim.bottom(1)[0].date
		var maxDate = dateDim.top(1)[0].date
		var datesScale = d3.time.scale().domain([minDate, maxDate])

		var composite = dc.compositeChart("#game-dates-composed");
		var scrubberChart = dc.barChart('#scrubber-chart');

		//composite chart render line chart with scatterplot to mark games
		composite
	     .width(950)
	     .height(480)
	     .x(datesScale)
		 .margins({top: 10, right: 50, bottom: 60, left: 70})
		 .rangeChart(scrubberChart)
	     .renderHorizontalGridLines(true)
		 .mouseZoomable(true)
		// .onClick()



		.on('renderlet', function(chart) {
				  chart.selectAll('circle.dot')
					  .on('mouseover.foo', function(d) {
						  console.log(d.x)
						chart.select('.display-games').text(d.key);
					})
					.on('mouseout.foo', function(d) {
						chart.select('.display-games').text('');
					})
		  })
	     .compose([
	         dc.lineChart(composite)
	             .dimension(dateDim)
	             .group(countsGroup)
		   		 .renderArea(true)
				 .transitionDuration(1000)

				 ,
	         dc.scatterPlot(composite)
	             .dimension(gameDateDim)
	             .colors('red')
	             .group(gameCountGroup)
		  .keyAccessor(function(d){ return d.key[0]})
		  .valueAccessor(function(d){ return d.value})



	         ])
	     .brushOn(false)

		 //scrubber chart allows to zzoom on composite chart
		 scrubberChart.width(950)
	         .height(40)
	         .margins({top: 0, right: 50, bottom: 20, left: 70})
	         .dimension(dateDim)
	         .group(countsGroup)
	         .gap(1000)
	         .x(datesScale)
	         .alwaysUseRounding(true)

	 	scrubberChart.yAxis().ticks(0);



		//var ndxg= crossfilter(GAME_DATES)
		var club1dim = ndxg.dimension(function(d){if (d.club1 != TEAM) {d.club2 = d.club1; d.club1 = TEAM} ; return d.club1})
		var club2dim = ndxg.dimension(function(d){return d.club2})
		var club1score = ndxg.dimension(function(d){return d.club1score})
		var club2score = ndxg.dimension(function(d){return d.club2score})


		 var //select1 = dc.selectMenu('#selectleague'),
		      select2 = dc.selectMenu('#selectclub1'),
		      select3 = dc.selectMenu('#selectclub2');
		     // datatable = dc.dataTable('#datatable');


			  select2
	      .dimension(club1dim)
	      .group(club1dim.group())
	      .controlsUseVisibility(true);
	    select3
	      .dimension(club2dim)
	      .group(club2dim.group())
	      .multiple(true)
	      .numberVisible(10)
	      .controlsUseVisibility(true);
	    // select3.dimension(stateDimension)
	    //   .group(stateDimension.group())
	    //   .multiple(true)
	    //   .numberVisible(10)
	    //   .controlsUseVisibility(true);
	    // datatable
	    //   .dimension(letterDimension2)
	    //   .group(function(d) { return d.letter; })
	    //   .columns(['color', 'state'])
	    //   .size(data.length);


		var table = dc.dataTable("#game-table");
		table
		    .width(768)
		    .height(480)
		    .dimension(gameDateDim)
		    .group(function(d){console.log(d); return d})
		    .columns([function (d) { return gameDateFormat(d.date)},
				function (d) { console.log(d);return d.club1},
					function (d) { return d.club1score},
					function (d) { return d.club2},
					function (d) { return d.club2score}
					])
		    .sortBy(function (d) { return d.date })




	dc.renderAll()
});


// how will I get the games into a table? -- lose all data except x and y  crossfilter between table and graph?
//pie chart of wins and losses



//TODO data table of game info
