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
       getGeotweets: function(club) {
           return $http.get('api/search/?q='+club).then(function(data) { 
               return data.data;
	   });
       }
   }
}])
.factory('TreemapService', ['$http', function($http){
   return {
       getLeagueCounts: function() {
           return $http.get('api/league').then(function(data) {
               return data.data;
           });
       }
   }
}]);
