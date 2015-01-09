var sparkingAdmin = angular.module('sparkingAdmin', ['ngRoute']);

sparkingAdmin.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

sparkingAdmin.config(function($routeProvider) {
    $routeProvider

        // route for the about page
        .when('/admin/clients/client', {
            templateUrl : '/admin/clients/client',
            controller  : 'dataController'
        })

        .when('/admin/clients/client/add', {
            templateUrl : '/admin/clients/client/add',
            controller  : 'dataController'
        })

        .when('/admin/clients/history', {
            templateUrl : '/admin/clients/history',
            controller  : 'dataController'
        })

});


sparkingAdmin.controller('dataController', function ($scope) {
  this.data = "a";
});
