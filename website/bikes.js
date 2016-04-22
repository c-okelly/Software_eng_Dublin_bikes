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
        // Determine call type and collect correct data
        var data_type = $("input[name=req_type]:checked").val();
        
        // Current data call
        if (data_type === "1"){
            $.getJSON("http://127.0.0.1:5000/Latest_Data", function(data) {
            json = data;
                console.log(data["Static_data"][0]);
                generate_markers_and_info_bubbles(data["Static_data"],data["Live_info"]);
            
            })
        }
        // Historical Load
        else if (data_type === "2"){ 
            var year = $("#hist_load_year").val();
            var month =$("#hist_load_month").val();
            var day = $("#hist_load_date").val();
            var hour = $("#hist_load_hour").val();
            var minute = $("#hist_load_min").val();
            
            var timestamp = parseInt(year + month + day + hour + minute);
            alert(timestamp);
            
            $.getJSON("http://127.0.0.1:5000/Historical_Call/"+timestamp, function(data) {
            json = data;
            console.log(data);
            })
        }
        // Historical hourly avaerage
        else if (data_type === "3"){
            var day_week = $("#hist_hour_day").val();
            var hour_day =  $("#hist_hour_hour").val();
            // "+day_week+"/"+hour_day
            $.getJSON("http://127.0.0.1:5000/Hourly_call/"+day_week+"/"+hour_day, function(data) {
            json = data;
            console.log(data);
            })
        }
};

// static_data, info_bubble_content

var generate_markers_and_info_bubbles = function(static_data, info_bubble_content) {
    var no_stations = static_data["no_stations"]
    console.log(no_stations);
    
    for (i=0;i<100;i++) {
        alert(i);
        
        marker = new google.maps.Marker({
            map: map,
            icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
            draggable: false,
            animation: google.maps.Animation.DROP,
            position: {lat: static_data[i]["Lat"], lng: static_data[i]["Long"]}
            });
        
        var info_content = '<div class="phoneytext"><p><br><br> hi</p></div>';
        
        infoBubble = new InfoBubble({
              map: map,
              content: info_content,
              shadowStyle: 1,
              padding: 0,
              backgroundColor: 'yellow',
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
                    infoBubble.setContent(static_data[i][0]);
                    infoBubble.open(map, marker);
                }
            })(marker, i));
    };
}

