angular.module('PartyParrots')
.factory('BackendService', ['$http', function($http) {
    return {
        getLeagueCounts: function(callback) {
            $http.get('/api/league')
            .then(function(data) {
                callback(data.data);
            });
        }
    }
}])
.factory('GeotweetsService',['$http', function($http){
   return {
       getGeotweets: function() {
           return $http.get('api/geotweets').then(function(data) { 
               return data.data;
	   });
       }
   }
}]);
