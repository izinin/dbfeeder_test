(function() {
  var underscore = angular.module('underscore', []);
  underscore.factory('_', function() {
    return window._; // assumes underscore has already been loaded on the page
  });
  var app = angular.module('cosmethics', ['underscore']);
  
  app.factory('singleton', function($rootScope) {
	  var singleton = {
	    searchFieldName: "category",
		  searchDBVal: "",
		  searchDBPrev: "",
		  updateResultSet: function(){
		    $rootScope.$broadcast('onUpdateResultSet');
		  }
	  };
	  return singleton;
  });

  app.directive("storeList",['singleton', '$http', '$log', 
                                       function(singleton, $http, $log){
	  return {
		  restrict: "E",
		  templateUrl: "/templates/store-list-products.html",
		  controller: function($scope){
		    this.updateResultSet = function(){
	        //guard code
	        if(!_.isEmpty(singleton.searchDBVal) && singleton.searchDBVal == singleton.searchDBPrev){
	          return;
	        }
	        
	        var self = this;
	        var par = (singleton.searchDBVal == singleton.searchDBPrev) ? 
	            {fname: singleton.searchFieldName, value: "ALL"} : 
	                {fname: singleton.searchFieldName, value: singleton.searchDBVal};
	        $http.get("/readdb", {params: {filter:par}})
	        .success(function(data){
	          self.products = data.store;
	          $log.log(self.products);
	        }).error(function(){
	          alert("server error");
	        });
		    };
		    
		    var self = this;
		    $scope.$on('onUpdateResultSet', function(){
		      self.updateResultSet();
        });
		    
		    this.updateResultSet();
		  },
		  controllerAs:"store"
	  };
  }]);
	
  app.directive("storeListSearch", ['singleton', '$log', function(singleton, $log){
    return {
      restrict: "E",
      templateUrl: "/templates/store-list-search.html",
      controller: function($scope,$timeout){
        var self = this;
        self.subj = "";
        $scope.isTimerRunning = false;
        $scope.dataChanged = function(value){
          if($scope.isTimerRunning){
            return;
          }
          $scope.isTimerRunning = true;
          
          $timeout(function(){
            $scope.isTimerRunning = false;
            singleton.searchDBPrev = singleton.searchDBVal;
            singleton.searchDBVal = value;
            singleton.updateResultSet();
          }, 1000);
        }
      },
      controllerAs:"storesearch"
    };
  }]);
})();
