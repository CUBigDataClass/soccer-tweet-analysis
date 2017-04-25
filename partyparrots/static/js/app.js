angular.module('PartyParrots', ['simpleAngularTicker'])
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});
