var app = angular.module('starter.controllers', []);

app.controller('DashCtrl', function(
  $scope,
  $state,
  $ionicPlatform,
  $cordovaGeolocation,
  $cordovaNetwork,
  $rootScope,
  $interval,
  $http,
  Preferences,
  $localstorage,
  $cordovaInAppBrowser,
  $cordovaSms
) {

  // Document ready
  $ionicPlatform.ready(function() {

    // Check if app is offline
    $rootScope.$on('$cordovaNetwork:online', function(event, networkState){
      $scope.offline = false;
    });
    $rootScope.$on('$cordovaNetwork:offline', function(event, networkState){
      $scope.offline = true;
    });

    // TTS
    $scope.playAudioGuide = function(){
      var mytext = 'Hello Hackers, I am Alexa your audio travel guide.';

      console.log("Data I want to display");
      var locationSpeechData = $localstorage.getObject("data");
      console.log("DAAAAAAAATAAA!");
      console.log(locationSpeechData);

      mytext += "In your near are the following locations. "

      for (var i = 0; i < 5; i++) {
        console.log(locationSpeechData[i].name);
        mytext += locationSpeechData[i].name + ". ";
      }
      mytext += 'And ' + locationSpeechData[5].name + ". If you have any questions just call me. I am happy to help you.";

      responsiveVoice.speak(mytext,  "UK English Female");
  $cordovaInAppBrowser
      /*
      var speech = new SpeechSynthesisUtterance(mytext);

      speech.lang = 'en-US';
      speechSynthesis.speak(speech);
      */
    };

    // Send SMS
    $scope.sendSMS = function(){
      var smsContent = $localstorage.get("lat") + ', ' + $localstorage.get("long");

      $cordovaSms
       .send('015735984082', smsContent, options)
       .then(function() {
         // Success! SMS was sent
         console.log("SMS send!");
       }, function(error) {
         // An error occurred
         console.log("Error - SMS");
         console.log(error);
       });
    }


    // Get direction
    $scope.getDirection = function(){
      console.log("Test");
      // Open Browser
        var options = {
          location: 'yes',
          clearcache: 'yes',
          toolbar: 'no'
        };

        var url = "http://maps.google.com/?q=";

        $cordovaInAppBrowser.open(url, '_blank', options)
          .then(function(event) {
            // success
            console.log(event);
          })
          .catch(function(event) {
            // error
            console.log(event);

          });
    };

    // Update the position for te first time
    updatePosition();

    $scope.refresh = function(){
      updatePosition();
      $scope.$broadcast('scroll.refreshComplete');
    }

    // Update the position every 10 sec
    setInterval(function(){
      updatePosition();
    }, 10000);

    function updatePosition(){
      // Get the current position and show it on a map
      var posOptions = {timeout: 10000, enableHighAccuracy: false};
      $cordovaGeolocation
        .getCurrentPosition(posOptions)
        .then(function (position) {
          var lat  = position.coords.latitude;
          var long = position.coords.longitude;

          $localstorage.set("lat", lat);
          $localstorage.set("long", long);

          console.log("Make preferences as a list");
          var preferencesArray = Preferences.get();
          var newPreferences = new Array();
          if(preferencesArray.food == true){
            newPreferences.push("food");
          }
          if(preferencesArray.nightlife == true){
            newPreferences.push("nightlife");
          }
          if(preferencesArray.restaurants == true){
            newPreferences.push("restaurants");
          }
          if(preferencesArray.shopping == true){
            newPreferences.push("shopping");
          }
          if(preferencesArray.freetime == true){
            newPreferences.push("freetime");
          }
          if(preferencesArray.culture == true){
            newPreferences.push("culture");
          }
          console.log(newPreferences);

          // Send post request
          myobject = { lat: position.coords.latitude, long: position.coords.longitude, preferences: newPreferences };

          var req =
          {
              method: 'POST',
              url: "http://b3afb221.ngrok.io/getInfo",
              data: myobject,
              headers: {'Content-Type': 'application/javascript'}
          }

          $http(req).
          success(function(data, status, headers, config)
          {
              //success
              console.log("Success");
              console.log(data);
              $scope.data = data;
              $localstorage.setObject("data", data);
          }).
          error(function(data, status, headers, config)
          {
              //error
              console.log("Error");
              console.log(data);
          });
      });
    }
  });
});


app.controller('AccountCtrl', function(
  $scope,
  $localstorage,
  Preferences
) {

    $scope.preferences = Preferences.get();

    $scope.updatePreferences = function(){
      console.log("Update the preferences");
      Preferences.set($scope.preferences);
      console.log(Preferences.get());
    }

});
