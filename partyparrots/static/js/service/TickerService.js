angular.module('PartyParrots')
.factory('TickerService', ['$http', function($http) {
    var tweet = null;
    return {
        getTweet: function() {
            return tweet;
        },
        fetchTweets: function() {
            $http.get('/api/realtime/')
            .then(function(data) {
                tweet = data.data.tweet
            });
        }
    }
}]);
