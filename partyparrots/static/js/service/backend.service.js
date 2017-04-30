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
	       var club_list = club.split(" ");
		   console.log(club_list);
		   var club_search = club_list.join("");
           return $http.get('api/search/?q='+club_search).then(function(data) { 
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
