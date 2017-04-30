angular.module('PartyParrots')
.factory('FrontendService', ['$http', function($http) {
    return {

        //don't quite understand
        getTeamCounts: function(callback) {
            console.log('in service')
            $http.get('/api/timeseries')
            .then(function(data) {
                callback(data.data);
            });
        }
    }
}]);
