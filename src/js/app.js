(function() {
  var underscore = angular.module('underscore', []);
  underscore.factory('_', function() {
    return window._; // assumes underscore has already been loaded on the page
  });
  var app = angular.module('cosmethics', ['underscore']);
  
  app.factory('singleton', function($rootScope) {
	  var singleton = {
		  searchDBVal: "",
		  serachDBPrev: ""
	  };
	  return singleton;
  });

  app.directive("storeList",['singleton', '$http', '$log', 
                                       function(singleton, $http, $log){
	  return {
		  restrict: "E",
		  templateUrl: "/templates/store-list-products.html",
		  controller: function(){
			  //guard code
			  if(!_.isEmpty(singleton.searchDBVal) && singleton.searchDBVal == singleton.serachDBPrev){
			    return;
			  }
			  
			  var self = this;
			  var par = (singleton.searchDBVal == singleton.serachDBPrev) ? 
					  {filter:"ALL"} : {filter:"singleton.searchDBVal"};
			  $http.get("/readdb", {params: par})
			  .success(function(data){
				  self.products = data.store;
				  $log.log(self.products);
			  }).error(function(){
				  alert("server error");
			  });
		  },
		  controllerAs:"store"
	  };
  }]);
	
})();
