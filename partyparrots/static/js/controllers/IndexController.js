angular.module('PartyParrots')
.controller('IndexController', ['BackendService', function(BackendService) {
    var self = this;

    self.createTreeMap = function(data) {
        var points = [];
        var clubsP;
        var leagueVal;
        var leagueI = 0;
        var clubP;
        var clubI = 0;
        var league;
        var club;

        for (league in data) {
            if (data.hasOwnProperty(league)) {
                leagueVal = 0;
                leagueP = {
                    id: 'id_' + leagueI,
                    name: league,
                    color: Highcharts.getOptions().colors[leagueI]
                };
                clubI = 0;
                for (club in data[league]) {
                    if (data[league].hasOwnProperty(club)) {
                        clubP = {
                            id: leagueP.id + '_' + clubI,
                            name: club,
                            parent: leagueP.id,
                            value: Math.round(+data[league][club]),
                            color: Highcharts.getOptions().colors[leagueI]

                        };
                        leagueVal += clubP.value;
                        points.push(clubP);
                        clubI = clubI + 1;
                    }
                }
                leagueP.value = Math.round(leagueVal);
                points.push(leagueP);
                leagueI = leagueI + 2;
            }
        }
        Highcharts.chart('treeMap', {
            series: [{
                type: 'treemap',
                layoutAlgorithm: 'squarified',
                allowDrillToNode: true,
                animationLimit: 1000,
                dataLabels: {
                    enabled: false
                },
                levelIsConstant: false,
                levels: [{
                    level: 1,
                    dataLabels: {
                        enabled: true
                    },
                    borderWidth: 3
                }],
                data: points
            }],
            subtitle: {
                text: 'Click points to drill down'
            },
            title: {
                text: 'Tweet Count across leagues and clubs since 2016'
            }
        });
    };

    self.initialize = function() {
        BackendService.getLeagueCounts(self.createTreeMap);
    }

    self.initialize();

}]);
