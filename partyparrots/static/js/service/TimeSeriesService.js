angular.module('PartyParrots')
.factory('TimeSeriesService', ['$http', function($http) {
    var tweet = null;
    return {
        fetchFixtures: function(club, callback) {
            $http.get('/api/fixtures/', {
                params: {
                    club: club
                }
            })
            .then(callback);
        },
        getDailyCounts: function(club, callback) {
            $http.get('/api/daily_tweet_counts/', {
                params: {
                    club: club
                }
            })
            .then(function(data) {
				callback(data);
	   		 });
        }
    }
}]);
