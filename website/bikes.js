$(document).ready(function () {
    $(".sub_button").click(function () {        
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

    // Reload map
    var reload_map = function() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 53.3498, lng: -6.2603},
      zoom: 13
    });
    // Load static data json file
//     var static_data = [];
//        $.ajax({
//          url: 'Dublin.json',
//          async: false,
//          dataType: 'json',
//          success: function (json) {
//            static_data = json;
//          }
//        });

////        console.log(static_data); // http://127.0.0.1:5000/    
        $.getJSON("http://127.0.0.1:5000/Static_Data", function(data) {
            json = data;
            console.log(data);
        })
        

        
    //Get data based on user request
        
    var data_list = [['first window',53.3498,-6.2603,.3],["second window",53.3498,-6.20,.8]];
        
    // Input data into map
    generate_markers_for_range(data_list);
    
    
    
};


var generate_markers_for_range = function(data_list) {
    for (i=0;i<2;i++) {
        
        marker = new google.maps.Marker({
            map: map,
            icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
            draggable: false,
            animation: google.maps.Animation.DROP,
            position: {lat: data_list[i][1], lng: data_list[i][2]}
            });
        
        infoBubble = new InfoBubble({
              map: map,
              content: '<div class="phoneytext"><p><br><br>'+data_list[i][0]+'</p></div>',
              shadowStyle: 1,
              padding: 0,
              backgroundColor: 'rgb(20,99,99)',
              borderRadius: 4,
              arrowSize: 10,
              borderWidth: 1,
              borderColor: '#2c2c2c',
              disableAutoPan: true,
              hideCloseButton: false,
              arrowPosition: 30,
              backgroundClassName: 'phoney',
              arrowStyle: 2
            });
            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infoBubble.setContent(data_list[i][0]);
                    infoBubble.open(map, marker);
                }
            })(marker, i));
    };
}

