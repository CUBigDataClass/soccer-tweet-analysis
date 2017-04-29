angular.module('PartyParrots')
.controller('TickerController', ['$timeout', 'TickerService', '$scope', function($timeout, TickerService, $scope) {
    var self = this;
    self.tickerItems = [{
        tweet: 'Live Tweets'
    }];

    // Initially set the ticker items to blank
    // TickerService.fetchTweets();

    $scope.$watch(function() {
        return TickerService.getTweet();
    }, function(oldValue, newValue) {
        if(newValue) {
            self.tickerItems.push({
                tweet: newValue
            });
        }
    });

    // Make request every 3 seconds
    // $timeout(function() {
    //     TickerService.fetchTweets();
    // }, 3000);
    setInterval(function() {
        TickerService.fetchTweets();
    }, 3000);

}]);
