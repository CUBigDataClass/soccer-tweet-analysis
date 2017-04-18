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
}]);
