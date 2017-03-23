angular.module('PartyParrots')
.service('ClubService', ['$http', function($http) {
    return {
        getClubs: function(callback) {
            $http.get('/api/getclubs')
            .then(function(response) {
                callback(response.data);
            });
        }
    }
}]);
