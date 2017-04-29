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
        var tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

        var options = {
        highlightOnMouseOver: true,
        maxDepth: 1,
        maxPostDepth: 2,
        minColor: '#cceaea',
        midColor: '#99d6d6',
        maxColor: '#66c1c1',
        minHighlightColor: '#e8f0f0',
        midHighlightColor: '#cbdede',
        maxHighlightColor: '#b5d0d0',
        headerHeight: 15,
        headerColor: '#ee8100',
        showScale: true,
        height: 500,
        fontSize: 14, 
        fontFamily: 'Roboto Condensed', 
        textStyle: {bold:true},
        useWeightedAverageForAggregation: true,
        generateTooltip: showStaticTooltip
      };
        tree.draw(mapData, options);

        function showStaticTooltip(row, size, value) {
           return '<div style="background:#fff; padding:10px; border:solid 1px #ccc; font-family: Roboto Condensed">' + size + ' tweets</div>';
        }
        });
    };
    
    google.charts.load('current', {'packages':['treemap']});
    google.charts.setOnLoadCallback(this.treeMap);
}]);
