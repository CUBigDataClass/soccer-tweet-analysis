angular.module('PartyParrots')
.service('StateService', [function() {
    var state = 'timeseries';

    return {
        setState: function(newState) {
            state = newState;
        },
        getState: function() {
            return state;
        }
    }
}]);
