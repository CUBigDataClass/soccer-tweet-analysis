angular.module('PartyParrots')
.controller('GeomapController', [function() {
    var self = this;

    this.clubIcon = function(club) {
         var icon = L.icon({
	     iconUrl: '../static/img/' + club + '.png', 
             iconSize: [40, 40],
             iconAnchor: [10, 10],
	 });
         return icon;
    };

    this.geoMap = function() {
                var lfcLogo = this.clubIcon('lfc');
             
                var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
                        }),
                latlng = L.latLng(-37.82, 175.24);

                var map = L.map('geo-map', {center: latlng, zoom: 13, layers: [tiles]});

                var markers = L.markerClusterGroup();
 
                for (var i = 0; i < addressPoints.length; i++) {
                        var a = addressPoints[i];
                        var title = a[2];
                        var marker = L.marker(new L.LatLng(a[0], a[1]), {icon: lfcLogo, title: title });
                        marker.number = a[2];
                        marker.bindPopup(title);
                        markers.addLayer(marker);
                }

                map.addLayer(markers);
    };

    this.geoMap();

}]);
