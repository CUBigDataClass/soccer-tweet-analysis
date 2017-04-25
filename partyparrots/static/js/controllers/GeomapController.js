angular.module('PartyParrots').controller('GeomapController', ['GeotweetsService', function(GeotweetsService) {
    var self = this;
    var geoPoints = GeotweetsService.getGeotweets();

    this.geoMap = function() {
        geoPoints.then(function(geoPoints){
            var points = geoPoints["data"].replace(/'/g,'"');
            var points = JSON.parse(points);
            var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                maxZoom:18,
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
            }),
            latlng = L.latLng(0, 0);
    
            var map = L.map('geo-map', {center: latlng, zoom: 2, layers: [tiles]});
    
            var markers = L.markerClusterGroup({chunkedLoading:true});
    
            for (var i = 0; i < points.length; i++) {
                    var a = points[i]; 
                    var title = a['text'];
                    var marker = L.marker(new L.LatLng(a['lat'], a['lon']), {title: title});
                    marker.bindPopup(title);
                    markers.addLayer(marker);
            }
    
            map.addLayer(markers);
        });   
    };
    
    this.geoMap();
}]);
