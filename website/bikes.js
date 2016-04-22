$(document).ready(function () {
    $(".sub_button").click(function () {        
        dublin_city_coord = [53.3498, -6.2603]
        reload_map(dublin_city_coord);
        
        
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
    var reload_map = function(city_coord) {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: city_coord[0], lng: city_coord[1]},
      zoom: 13
    });
        // Determine call type and collect correct data
        var data_type = $("input[name=req_type]:checked").val();
        
        // Current data call
        if (data_type === "1"){
            $.getJSON("http://127.0.0.1:5000/Latest_Data", function(data) {
                json = data;
//                console.log(data["Station_info"][0]);
                generate_markers_and_info_bubbles(data["Static_data"],data["Station_info"]);
            
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
                generate_markers_and_info_bubbles(data["Static_data"],data["Station_info"]);
            })
        }
        // Historical hourly avaerage
        else if (data_type === "3"){
            var day_week = $("#hist_hour_day").val();
            var hour_day =  $("#hist_hour_hour").val();
            // "+day_week+"/"+hour_day
            $.getJSON("http://127.0.0.1:5000/Hourly_call/"+day_week+"/"+hour_day, function(data) {
                json = data;
//                console.log(data["Station_info"]);
                generate_markers_and_info_bubbles(data["Static_data"],data["Station_info"]);
            })
        }
};

// static_data, info_bubble_content

var generate_markers_and_info_bubbles = function(static_data, info_bubble_content) {
    var no_stations = static_data["no_stations"];
    var green_icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
    var yellow_icon = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png";
    var red_icon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";

    var content_array_live = []; 
    
    for (i=0;i<no_stations;i++) {
        alert(i);
        
        // Set percent full
        var percent_full = (info_bubble_content[i]["Available_bikes"] / info_bubble_content[i]["No_bike_stands"]);
        // Set icon of current station
        var icon_set = "";
        if (percent_full >= 0.6) {icon_set =green_icon;}
        else if (percent_full >= 0.2) {icon_set =yellow_icon;}
        else if (percent_full <= 0.2) {icon_set =red_icon;}
        // Create marker and place
        marker = new google.maps.Marker({
            map: map,
            icon: icon_set,
            draggable: false,
            animation: google.maps.Animation.DROP,
            position: {lat: static_data[i]["Lat"], lng: static_data[i]["Long"]}
            });
        
        // Generate content
        var content_for_station = '<div><img src="images/Dublin_bikes_logo.jpg"  style="width:160px;">\
                        <p style="color:white; align:left;">\
                        Info for station no '+info_bubble_content[i]["Station_no"]+'<br>\
                        There are a total of '+info_bubble_content[i]["No_bike_stands"].toFixed(0)+' bike stands<br>\
                        There are '+info_bubble_content[i]["Available_bikes"].toFixed(1)+' bikes availiable<br>\
                        There are '+info_bubble_content[i]["Available_bike_stands"].toFixed(1)+' bikes stands availiable\
                        \</p></div>';
        
        content_array_live.push(content_for_station);
        
        // Create general info bubble
        infoBubble = new InfoBubble({
            map: map,
            content: "Blank",
            shadowStyle: 1,
            padding: 0,
            backgroundColor: '#084C55',
            borderRadius: 0,
            arrowSize: 20,
            borderWidth: 1,
            borderColor: '#2c2c2c',
            disableAutoPan: true,
            hideCloseButton: false,
            arrowPosition: 30,
            maxWidth: 200,
            maxHeight: 140,
            backgroundClassName: '',
            arrowStyle: 2
            });
            // On click load info into info bubble and open
            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infoBubble.setContent(content_array_live[i]);
                    infoBubble.open(map, marker);
                }
            })(marker, i));
    };
}

