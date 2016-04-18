$(document).ready(function () {
    $(".sub_button").click(function () {
    alert("Hello");
    reload_map();
    });
});

                  
// Based of the Google maps Api documentation
// Load first map for screen
var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 53.3498, lng: -6.2603},
      zoom: 13
    });
};


// Fucntion that will load in Dublin bikes load markers depending on SQL data
var reload_map = function() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 53.3498, lng: -6.2603},
      zoom: 13
    });
    marker = new google.maps.Marker({
    map: map,
    draggable: true,
    animation: google.maps.Animation.DROP,
    position: {lat: 53.3498, lng: -6.2603}
  })
};