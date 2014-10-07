(function() {
  var app = angular.module('cosmethics', []);

  app.directive("storeList", ['$http', '$log', function($http, $log){
	return {
		restrict: 'E',
		templateUrl: "/templates/store-list-products.html",
		controller:   function(){
		    var self = this;
		    $http.get("/readdb").success(function(data){
		    	self.products = data.store;
		    	$log.log(self.products);
		    }).error(function(){
		    	alert("error");
		    });    
		  },
		controllerAs:"store"
	};
  }])
	
})();
