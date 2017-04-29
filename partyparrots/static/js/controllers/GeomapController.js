angular.module('PartyParrots').controller('GeomapController', ['$scope', 'GeotweetsService', function($scope, GeotweetsService) {
    var self = this;
    $scope.searchField = 'Arsenal';
  
    this.mapInitialize = function() {
        var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
             maxZoom:18,
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
            }),
            latlng = L.latLng(0, 0);

            var map = L.map('geo-map', {center: latlng, zoom: 2, layers: [tiles]});
            return map;
    };

    this.markers = L.markerClusterGroup({chunkedLoading:true});
    this.geoMap = function(map) {
        var geoPoints = GeotweetsService.getGeotweets($scope.searchField);
        geoPoints.then(function(geoPoints){
            var points = geoPoints["results"];
            for (var i = 0; i < points.length; i++) {
                    var a = points[i]['_source'];
                    var title = a['text'];
                    var marker = L.marker(new L.LatLng(a['lat'], a['lon']), {title: title});
                    marker.bindPopup(title);
                    self.markers.addLayer(marker);
            }
    
            map.addLayer(self.markers);
        });   
    };
  
    this.map = this.mapInitialize();

    $scope.search =  function() { 
        self.markers.clearLayers();
        self.geoMap(self.map);
    };
    $scope.search(); 
}]);
