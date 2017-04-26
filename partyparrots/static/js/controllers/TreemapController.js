angular.module('PartyParrots').controller('TreemapController', ['TreemapService', function(TreemapService) {
    var self = this;
    var data = TreemapService.getLeagueCounts();
    
    this.treeMap = function() {
        var mapData = new google.visualization.DataTable();
        mapData.addColumn('string', 'ID');
        mapData.addColumn('string', 'Parent');
        mapData.addColumn('number', 'Count');

        var arrData = [];
        data.then(function(data) { 
            arrData.push(['Leagues', null, 0]);
            for(var league in data) {
                arrData.push([league,'Leagues', null]);
                for(var club in data[league]) {
                    arrData.push([club, league, data[league][club]]);
                }
            }
        mapData.addRows(arrData);
        console.log(arrData[0]);
        var tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

        var options = {
        highlightOnMouseOver: true,
        maxDepth: 1,
        maxPostDepth: 2,
        minHighlightColor: 'feeb65',
        midHighlightColor: '#e4521b',
        maxHighlightColor: '#4d342f',
        minColor: '#ffeda0',
        midColor: '#feb24c',
        maxColor: '#f03b20',
        headerHeight: 15,
        showScale: true,
        height: 500,
        fontSize: 14, 
        fontFamily: 'Roboto Condensed', 
        textStyle: {bold:true, auraColor: '#fff'},
        useWeightedAverageForAggregation: true,
        generateTooltip: showStaticTooltip
      };
        console.log(mapData);
        tree.draw(mapData, options);

        function showStaticTooltip(row, size, value) {
           return '<div style="background:#fff; padding:10px; border:solid 1px #ccc">' + size + ' tweets</div>';
        }
        });
    };
    
    google.charts.load('current', {'packages':['treemap']});
    google.charts.setOnLoadCallback(this.treeMap);
}]);
