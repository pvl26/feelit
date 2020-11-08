jQuery(function() {

    $('#get_city').on("click", function(){
        getCoordintes(); 
    })

    emotions = [
        "happy",
        "hopeful",
        "adventure",
        "chill",
        "dreamy",
        "sad"
    ]
    $('#edit_moods').on("click", function(){
        $("#done_moods").removeAttr("hidden")
        for(i = 0; i < 6; i++) {
            $(`#cm${emotions[i]}`).removeAttr("hidden")
            $(`#cp${emotions[i]}`).removeAttr("hidden")
            $(`#gm${emotions[i]}`).removeAttr("hidden")
            $(`#gp${emotions[i]}`).removeAttr("hidden")

            
        }
    })
    dict_current = {
        "happy" : 0,
        "hopeful" : 0, 
        "adventure" : 0,
        "chill" : 0,
        "dreamy" : 0,
        "sad" : 0,
    }
    dict_goal = {
        "happy" : 0,
        "hopeful" : 0, 
        "adventure" : 0,
        "chill" : 0,
        "dreamy" : 0,
        "sad" : 0,
    }
    for(i = 0; i < 6; i++) {
        $(`#cm${emotions[i]}`).on("click", function() {
            $(`#c${$(this).attr("bar")}`).css({
                'width' : $(`#c${$(this).attr("bar")}`).width()  * 0.8
            });
            dict_current[`${$(this).attr("bar")}`] -= 1;
        })
        $(`#cp${emotions[i]}`).on("click", function() {
            $(`#c${$(this).attr("bar")}`).css({
                'width' : $(`#c${$(this).attr("bar")}`).width()  * 1.2
            });
            dict_current[`${$(this).attr("bar")}`] += 1;
            
        })
        $(`#gm${emotions[i]}`).on("click", function() {
            $(`#g${$(this).attr("bar")}`).css({
                'width' : $(`#g${$(this).attr("bar")}`).width()  * 0.8
            });
            console.log(`#g${$(this).attr("bar")}`)
            dict_goal[`${$(this).attr("bar")}`] -= 1;

        })
        $(`#gp${emotions[i]}`).on("click", function() {

            $(`#g${$(this).attr("bar")}`).css({
                'width' : $(`#g${$(this).attr("bar")}`).width()  * 1.2
            });

            dict_goal[`${$(this).attr("bar")}`] += 1;
            
        })
   
    }

    $('#done_moods').on("click", function() {
        $("#done_moods").attr("hidden", true);
        for(i = 0; i < 6; i++) {
            $(`#cm${emotions[i]}`).attr("hidden", true)
            $(`#cp${emotions[i]}`).attr("hidden", true)
            $(`#gm${emotions[i]}`).attr("hidden", true)
            $(`#gp${emotions[i]}`).attr("hidden", true)
            
        }

        dict = {
            "current"  : dict_current,
            "goal" : dict_goal
        }
        
       
        const csrftoken = Cookies.get('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          });
           $.ajax({
              type: 'POST',
              url: $('#done_moods').attr("action"),
              data: dict,
              name: 'new_data'
          }).done(function(data) {
              if(data["status"] == "fail") {
                console.log("here");
                $("#error").show();
                $("#error").text("Invalid credentials");
              } else {
                // window.location.reload()
              }
          });
        

    })
    

})

function getCoordintes() { 
    var options = { 
        enableHighAccuracy: true, 
        timeout: 5000, 
        maximumAge: 0 
    }; 
  
    function success(pos) { 
        var crd = pos.coords; 
        var lat = crd.latitude.toString(); 
        var lng = crd.longitude.toString(); 
        var coordinates = [lat, lng]; 
        console.log(`Latitude: ${lat}, Longitude: ${lng}`); 
        getCity(coordinates); 
        return; 
  
    } 
  
    function error(err) { 
        console.warn(`ERROR(${err.code}): ${err.message}`); 
    } 
  
    navigator.geolocation.getCurrentPosition(success, error, options); 
} 
  
// Step 2: Get city name 
function getCity(coordinates) { 
    var xhr = new XMLHttpRequest(); 
    var lat = coordinates[0]; 
    var lng = coordinates[1]; 
  
    // Paste your LocationIQ token below. 
    xhr.open('GET', "https://us1.locationiq.com/v1/reverse.php?key=pk.b09009f32c0ef71aac3476b5a5849b3f&lat=" + 
    lat + "&lon=" + lng + "&format=json", true); 
    xhr.send(); 
    xhr.onreadystatechange = processRequest; 
    xhr.addEventListener("readystatechange", processRequest, false); 
  
    function processRequest(e) { 
        if (xhr.readyState == 4 && xhr.status == 200) { 
            var response = JSON.parse(xhr.responseText); 
            var city = response.address.city;
            console.log(city); 
            const csrftoken = Cookies.get('csrftoken');
            dict = {
                'city' : city
            }
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
              });
               $.ajax({
                  type: 'POST',
                  url: $('#get_city').attr("action"),
                  data: dict,
              }).done(function(data) {
                    location.reload();
              });
            return; 
        } 
    } 
} 